# studposts_server
Cистема (подкодовым названием - "Лента ВК") представляет собой веб-приложение, напоминающее ленту социальной сети, построенное на Flask. Она использует PostgreSQL для хранения данных, JWT для аутентификации и Redis для 
кэширования. Незарегистрированные пользователи могут просматривать посты, в то время как зарегистрированные пользователи могут создавать посты, комментировать и ставить лайки. CAPTCHA используется для защиты от ботов при 
регистрации и входе

**Стек технологий:**

- **Python Flask**: Легковесный фреймворк, который хорошо подходит для создания RESTful API.
- **PostgreSQL**: Надежная и мощная реляционная база данных, которая хорошо масштабируется.
- **Redis**: Быстрая база данных в памяти, идеальна для кэширования и управления сессиями.
- **JWT (JSON Web Tokens)**: Безопасный способ аутентификации и авторизации пользователей.
- **CAPTCHA**: Защита от спама и автоматизированных ботов при регистрации и авторизации.
