# Database Setup for Idea Submission Form

This directory contains the necessary SQL scripts and documentation for setting up the database infrastructure to support the idea submission form on the intranet.

## 1. Database Choice

For this feature, we will utilize an existing central MySQL database instance (e.g., `intranet_db`). If a new dedicated database is required in the future, follow standard provisioning procedures.

## 2. Table Creation

The `ideas` table will be created using the `schema.sql` script. This table will store all submitted ideas.

### Table Columns:

- `id`: Primary key, auto-incrementing integer.
- `title`: VARCHAR (255), not null. The title of the idea.
- `description`: TEXT. A detailed description of the idea.
- `submitter_name`: VARCHAR (255). The name of the employee who submitted the idea.
- `submitter_email`: VARCHAR (255). The email of the employee who submitted the idea.
- `submission_timestamp`: TIMESTAMP, defaults to the current timestamp. Records when the idea was submitted.

## 3. Indexing

A B-tree index will be created on the `submission_timestamp` column to optimize queries that retrieve ideas based on their submission time (e.g., displaying the latest ideas).

## 4. Data Integrity

- `id` as `AUTO_INCREMENT` and `PRIMARY KEY` ensures uniqueness and efficient row identification.
- `title` is marked `NOT NULL` to ensure every idea has a title.
- Data types are chosen to accommodate the expected data (e.g., `TEXT` for potentially long descriptions).

## 5. Backup and Recovery

Since this table will reside within an existing central database (`intranet_db`), it will automatically benefit from the existing enterprise-level backup and recovery strategies already implemented for that database. These typically include:

- **Daily full backups:** Entire database snapshots taken regularly.
- **Point-in-time recovery (PITR):** Transaction logs are typically maintained to allow restoration to any specific point in time.
- **Geographical redundancy:** Backups may be replicated to different data centers.

**No additional configuration is required specifically for the `ideas` table beyond ensuring the central database's existing backup policies are robust and regularly tested.**

## 6. Database Credentials and Access

Database credentials and access permissions for the `intranet_db` will be managed through our central secrets management system (e.g., HashiCorp Vault, AWS Secrets Manager). The backend service responsible for interacting with this database will be granted read/write access to the `ideas` table. Specific steps are TBD by the platform team based on our established access control policies:

1.  **Create a dedicated database user** for the backend service (e.g., `intranet_ideas_service_user`).
2.  **Grant `SELECT`, `INSERT`, `UPDATE`, `DELETE` permissions** on the `intranet_db.ideas` table to this user.
3.  **Store the credentials securely** in the secrets management system.
4.  **Configure the backend service** to retrieve these credentials at runtime.

**Example GRANT statement (to be executed by a DBA):**

```sql
GRANT SELECT, INSERT, UPDATE, DELETE ON intranet_db.ideas TO 'intranet_ideas_service_user'@'localhost' IDENTIFIED BY 'your_secure_password';
FLUSH PRIVILEGES;
```

*(Note: Replace `your_secure_password` with a strong, generated password and `localhost` with the actual host/IP of the backend service if different.)*

This setup ensures that the `ideas` table is properly integrated into our existing database infrastructure, benefiting from established security, performance, and reliability practices.