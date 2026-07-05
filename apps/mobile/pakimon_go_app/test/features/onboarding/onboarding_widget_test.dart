import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/onboarding/domain/onboarding_service.dart';
import 'package:pakimon_go_app/features/onboarding/presentation/onboarding.dart';

class _MemStore implements OnboardingStore {
  bool seen = false;

  @override
  Future<bool> hasSeen() async => seen;

  @override
  Future<void> markSeen() async => seen = true;
}

Widget _wrap(OnboardingService service) => MaterialApp(
      home: OnboardingGate(
        service: service,
        child: const Scaffold(body: Text('APP HOME')),
      ),
    );

void main() {
  testWidgets('shows onboarding on first launch', (tester) async {
    await tester.pumpWidget(_wrap(OnboardingService(store: _MemStore())));
    await tester.pumpAndSettle();

    expect(find.text('Welcome to PakimonGO'), findsOneWidget);
    expect(find.text('APP HOME'), findsNothing);
  });

  testWidgets('Skip completes onboarding', (tester) async {
    final store = _MemStore();
    await tester.pumpWidget(_wrap(OnboardingService(store: store)));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Skip'));
    await tester.pumpAndSettle();

    expect(find.text('APP HOME'), findsOneWidget);
    expect(store.seen, true);
  });

  testWidgets('paging to the end and Get started completes', (tester) async {
    final store = _MemStore();
    await tester.pumpWidget(_wrap(OnboardingService(store: store)));
    await tester.pumpAndSettle();

    for (var i = 0; i < 3; i++) {
      await tester.tap(find.text('Next'));
      await tester.pumpAndSettle();
    }
    expect(find.text('Get started'), findsOneWidget);

    await tester.tap(find.text('Get started'));
    await tester.pumpAndSettle();

    expect(find.text('APP HOME'), findsOneWidget);
    expect(store.seen, true);
  });

  testWidgets('already-seen skips onboarding', (tester) async {
    final store = _MemStore()..seen = true;
    await tester.pumpWidget(_wrap(OnboardingService(store: store)));
    await tester.pumpAndSettle();

    expect(find.text('APP HOME'), findsOneWidget);
    expect(find.text('Welcome to PakimonGO'), findsNothing);
  });
}
