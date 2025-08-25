# cloudbuild-multi-triggers-demo
Showcasing how to use substitutions with a single Cloud Build YAML to handle multiple projects.

GitHub (cloudbuild-multi-triggers-demo)
        │  (push/PR)
        ▼
Cloud Build (Triggers: unixtime-build, passgen-build)
        │   build & push
        ▼
Artifact Registry (images)
        │   deploy
        ▼
Cloud Run: api-unixtime      Cloud Run: api-passgen
          \                    /
           \                  /
            ▼                ▼
             API Gateway (x-api-key, quotas)
                    │
                 Clients