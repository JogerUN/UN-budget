
ddddddddddddddddd
``` mermaid
erDiagram
    USER ||--o{ BUDGET : defines
    USER ||--o{ CATEGORY : creates
    USER ||--o{ PAYMETHOD : manages
    USER ||--o{ INCOME : logs
    USER ||--o{ EXPENSE : logs

    BUDGET ||--|{ CATEGORY_BUDGET : contains
    CATEGORY ||--o{ CATEGORY_BUDGET : allocated
    CATEGORY ||--o{ EXPENSE : classifies
    PAYMETHOD ||--o{ EXPENSE : funds

    USER {
        uuid id PK
        string first_name
        string last_name
        string email UK
        string password_hash
        timestamp registration_date
    }

    BUDGET {
        uuid id PK
        uuid user_id FK
        int month
        int year
        string currency
        timestamp created_at
    }

    CATEGORY {
        uuid id PK
        uuid user_id FK "nullable for system defaults"
        string name
        enum type "Need, Want, Savings/Debt"
        boolean is_custom
    }

    PAYMETHOD {
        uuid id PK
        uuid user_id FK
        string name
        enum type "Bank, Cash, Digital Wallet"
        boolean is_active
    }

    CATEGORY_BUDGET {
        uuid id PK
        uuid budget_id FK
        uuid category_id FK
        numeric allocated_amount
    }

    EXPENSE {
        uuid id PK
        uuid user_id FK
        uuid category_id FK
        uuid paymethod_id FK
        numeric amount_cop
        date date
        enum record_state "Active, Cancelled"
        timestamp created_at
        timestamp updated_at
    }

    INCOME {
        uuid id PK
        uuid user_id FK
        string source
        numeric amount_cop
        date expected_date
        date actual_date
        enum record_state "Expected, Received, Cancelled"
        timestamp created_at
        timestamp updated_at
    }
```

dddddddddddddddddddddddd