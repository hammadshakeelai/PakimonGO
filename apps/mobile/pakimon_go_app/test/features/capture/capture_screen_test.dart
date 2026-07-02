import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/features/capture/presentation/capture_screen.dart';

void main() {
  testWidgets('CaptureScreen renders form fields',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: CaptureScreen()),
    );
    await tester.pumpAndSettle();

    expect(find.text('Test Capture'), findsOneWidget);
    expect(find.text('Context'), findsOneWidget);
    expect(find.text('Species'), findsOneWidget);
    expect(find.text('Cute Name'), findsOneWidget);
    expect(find.text('Caption'), findsOneWidget);
    expect(find.text('Submit Capture'), findsOneWidget);
  });

  testWidgets('CaptureScreen shows status text after submit',
      (WidgetTester tester) async {
    await tester.pumpWidget(
      const MaterialApp(home: CaptureScreen()),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.text('Submit Capture'));
    await tester.pump();

    expect(find.text('Test Capture'), findsOneWidget);
    expect(find.text('Submitting...'), findsNothing);
  });
}
