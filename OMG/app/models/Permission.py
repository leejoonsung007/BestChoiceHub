class Permission:
    USER_LIKE = 1      # 关注school
    COMMENTS = 2    # 写comments
    COMMENTS_MANAGEMENT = 4  # 管理他人发表的评论
    POST_SCHOOL_INFORMATION = 8 #post学校信息
    SCHOOL_INFORMATION_MANAGEMENT = 16 #管理学校信息
    MODERATE = 32 # 协调者权限 - 不知是否多余 先留着
    ACCOUNT_MANAGEMENT = 64 #账号管理
    ADMINISTRATOR = 128      # 管理者权限