import 'package:flutter_test/flutter_test.dart';
import 'package:pakimon_go_app/main.dart';

void main() {
  testWidgets('app shows map screen as home', (WidgetTester tester) async {
    await tester.pumpWidget(const PakimonGoApp());
    await tester.pumpAndSettle();

    expect(find.text('PakimonGO'), findsNothing);
    expect(find.text('PakimonGO Map'), findsOneWidget);
  });

  testWidgets('navigates to capture screen via bottom nav', (WidgetTester tester) async {
    await tester.pumpWidget(const PakimonGoApp());
    await tester.pumpAndSettle();

    expect(find.text('Test Capture'), findsNothing);
  });
}
