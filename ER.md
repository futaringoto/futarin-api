# ER図
以下にER図を示す
## ver. 2024/10/10

```mermaid
erDiagram
    raspi ||--|| user : ""
    user }|--|| couple : ""
    user ||--o{ message : ""

    raspi {
        int_unsigned id PK "ラズパイID"
        varchar(20) name "ラズパイ名"
        varchar(50) connection_id "コネクションID"
        timestamp created_at "作成日時"
        timestamp updated_at "更新日時"
    }

    user {
        int_unsigned id PK "ユーザID"
        int_unsigned couple_id FK "所属するCoupleのID (null許容, on_delete_set_null)"
        varchar(20) name "ユーザー名"
        int_unsigned raspi_id FK "使用するラズパイのID (null許容, on_delete_set_null)"
        varchar(45) thread_id "OpenAI AssistantsのThreadのID"
        timestamp created_at "作成日時"
        timestamp updated_at "更新日時"
    }

    couple {
        int_unsigned id PK "ペアのID"
        varchar(20) name "ペアの名前"
        timestamp created_at "作成日時"
        timestamp updated_at "更新日時"
    }

    message {
        int_unsigned id PK "メッセージID"
        int_unsigned user_id FK "ユーザー名"
        varchar(1000) content "メッセージの内容"
        timestamp created_at "作成日時"
    }
```
