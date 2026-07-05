/// Neutral 13+ age gate (FR-AGE-001..003). Collects a birth year without
/// revealing the threshold, blocks under-13, and records a coarse band
/// (teen 13–17 / adult 18+) for stricter defaults later.
library;

enum AgeGateStatus { unknown, blocked, verified }

enum AgeBand { teen, adult }

class AgeGateOutcome {
  final AgeGateStatus status;
  final AgeBand? band;
  const AgeGateOutcome(this.status, [this.band]);
}

/// Persistence for the gate decision. Kept minimal so it is trivially
/// testable without the shared_preferences plugin.
abstract class AgeGateStore {
  Future<String?> read();
  Future<void> write(String value);
}

class AgeGateService {
  static const int minAge = 13;
  static const int _adultAge = 18;

  final AgeGateStore _store;
  final int Function() _currentYear;

  AgeGateService({required AgeGateStore store, int Function()? currentYear})
      : _store = store,
        _currentYear = currentYear ?? (() => DateTime.now().year);

  Future<AgeGateOutcome> load() async {
    final raw = await _store.read();
    if (raw == null || raw.isEmpty) {
      return const AgeGateOutcome(AgeGateStatus.unknown);
    }
    if (raw == 'blocked') return const AgeGateOutcome(AgeGateStatus.blocked);
    if (raw.startsWith('verified:')) {
      final band = raw.endsWith('adult') ? AgeBand.adult : AgeBand.teen;
      return AgeGateOutcome(AgeGateStatus.verified, band);
    }
    return const AgeGateOutcome(AgeGateStatus.unknown);
  }

  /// Records [birthYear] and returns the resulting gate outcome, persisting it.
  Future<AgeGateOutcome> submitBirthYear(int birthYear) async {
    final age = _currentYear() - birthYear;
    if (age < minAge) {
      await _store.write('blocked');
      return const AgeGateOutcome(AgeGateStatus.blocked);
    }
    final band = age < _adultAge ? AgeBand.teen : AgeBand.adult;
    await _store.write('verified:${band.name}');
    return AgeGateOutcome(AgeGateStatus.verified, band);
  }
}
