/// First-run onboarding (FR-ONB-001..005): safety, privacy, and scoring-honesty
/// education shown once. Persistence is behind a tiny interface so it is
/// testable without the shared_preferences plugin.

abstract class OnboardingStore {
  Future<bool> hasSeen();
  Future<void> markSeen();
}

class OnboardingService {
  final OnboardingStore _store;

  OnboardingService({required OnboardingStore store}) : _store = store;

  Future<bool> isComplete() => _store.hasSeen();

  Future<void> complete() => _store.markSeen();
}
