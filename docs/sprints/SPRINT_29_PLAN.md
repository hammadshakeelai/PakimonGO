# Sprint 29 Plan: Camera Plugin Integration

## Sprint Goal

Replace fake image bytes in the Flutter capture flow with real device camera/gallery capture using the `image_picker` plugin.

## Sprint Status

Complete.

## Sprint Backlog

| ID | Status | Task | Acceptance | Verification |
|---|---|---|---|---|---|
| S29-001 | Done | Add `image_picker` dependency to pubspec.yaml | `image_picker: ^1.1.2` in dependencies | `flutter pub get` succeeds |
| S29-002 | Done | Create `CaptureMediaService` interface + `ImagePickerService` | Abstract service with pickFromCamera/pickFromGallery; real impl uses ImagePicker | Interface supports mock injection |
| S29-003 | Done | Update `CaptureScreen` for real camera capture | Two-phase flow: select photo → preview → fill form → submit; Camera/Gallery buttons; image preview with error fallback | Camera tap invokes pickFromCamera, Gallery tap invokes pickFromGallery |
| S29-004 | Done | Write tests for camera integration | 4 new widget tests: form rendering, camera pick, gallery pick, broken image fallback | All 29 Flutter tests pass |

## File Ownership

| Area | Owner | Notes |
|---|---|---|
| `lib/features/capture/domain/capture_media_service.dart` | Mobile agent | Abstract service + result model |
| `lib/features/capture/data/image_picker_service.dart` | Mobile agent | ImagePicker implementation |
| `lib/features/capture/presentation/default_capture_media_service.dart` | Mobile agent | Factory for production wiring |
| `lib/features/capture/presentation/capture_screen.dart` | Mobile agent | Updated with camera/gallery UI |
| `lib/main.dart` | Mobile agent | Uses createDefaultMediaService() |
| `test/features/capture/capture_screen_test.dart` | Mobile agent | Widget tests |
| `test/widget_test.dart` | Mobile agent | App structure tests |
