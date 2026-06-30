# Infrastructure

Infrastructure code and configuration live here.

Planned areas:

- `database/`: migrations, seeds, fixtures, and restore drills.
- `docker/`: local development services.
- `firebase/`: Auth/App Check/Storage configuration notes and emulator setup.
- `terraform/`: cloud infrastructure once provider decisions are accepted.
- `cloud-run/`: service deployment manifests or blueprints.

No secrets should be committed. Use `.env.example` files for documented variables only.
