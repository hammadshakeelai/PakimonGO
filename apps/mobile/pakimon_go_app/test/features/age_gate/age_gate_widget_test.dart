import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/age_gate/domain/age_gate_service.dart';
import 'package:pakimon_go_app/features/age_gate/presentation/age_gate.dart';

class _MemStore implements AgeGateStore {
  String? value;

  @override
  Future<String?> read() async => value;

  @override
  Future<void> write(String v) async => value = v;
}

Widget _wrap(AgeGateService service) => MaterialApp(
      home: AgeGate(
        service: service,
        child: const Scaffold(body: Text('APP HOME')),
      ),
    );

AgeGateService _service(_MemStore store) =>
    AgeGateService(store: store, currentYear: () => 2026);

void main() {
  testWidgets('shows the birth-year prompt on first launch', (tester) async {
    await tester.pumpWidget(_wrap(_service(_MemStore())));
    await tester.pumpAndSettle();

    expect(find.text('What year were you born?'), findsOneWidget);
    expect(find.text('APP HOME'), findsNothing);
  });

  testWidgets('a valid adult year unlocks the app', (tester) async {
    await tester.pumpWidget(_wrap(_service(_MemStore())));
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField), '1990');
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();

    expect(find.text('APP HOME'), findsOneWidget);
  });

  testWidgets('an under-13 year shows the blocked screen', (tester) async {
    await tester.pumpWidget(_wrap(_service(_MemStore())));
    await tester.pumpAndSettle();

    await tester.enterText(find.byType(TextField), '2020'); // age 6
    await tester.tap(find.text('Continue'));
    await tester.pumpAndSettle();

    expect(find.textContaining('not eligible'), findsOneWidget);
    expect(find.text('APP HOME'), findsNothing);
  });

  testWidgets('a previously verified user skips the gate', (tester) async {
    final store = _MemStore()..value = 'verified:adult';
    await tester.pumpWidget(_wrap(_service(store)));
    await tester.pumpAndSettle();

    expect(find.text('APP HOME'), findsOneWidget);
    expect(find.text('What year were you born?'), findsNothing);
  });
}
