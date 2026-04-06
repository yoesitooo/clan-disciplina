class ActivityService:
    def __init__(
        self, 
        activity_repo, 
        profile_repo, 
        dispatcher: EventDispatcher,
        anti_spam: AntiSpamManager
    ):
        self.activity_repo = activity_repo
        self.profile_repo = profile_repo
        self.dispatcher = dispatcher
        self.anti_spam = anti_spam

    def log_activity(self, user_id: str, category: Category, photo_url: str) -> ActivityLog:
        # 1. Validación (Managers)
        ValidationManager.validate_evidence(photo_url)
        self.anti_spam.check_limit(user_id, category.id)

        # 2. Calcular XP
        xp_to_award = category.base_xp # Aquí podría entrar el XPService si es variable

        # 3. Guardar en DB
        activity = ActivityLog(
            id="uuid-generado", user_id=user_id, category_id=category.id, 
            photo_url=photo_url, xp_awarded=xp_to_award
        )
        self.activity_repo.save(activity)

        # 4. Actualizar Perfil y Evaluar Rango
        profile = self.profile_repo.get_by_user_id(user_id)
        profile.add_xp(xp_to_award)
        
        old_rank = profile.current_rank
        new_rank = RankService.calculate_rank(profile.total_xp)
        profile.current_rank = new_rank
        
        self.profile_repo.update(profile)

        # 5. Disparar Eventos
        self.dispatcher.dispatch(ActivityCreatedEvent(user_id, activity.id, xp_to_award))
        if old_rank != new_rank:
            self.dispatcher.dispatch(RankUpEvent(user_id, new_rank))

        return activity