import 'dart:io';
import 'dart:typed_data';

import 'package:image_picker/image_picker.dart';

import '../domain/capture_media_service.dart';

class ImagePickerService implements CaptureMediaService {
  final ImagePicker _picker;

  ImagePickerService({ImagePicker? picker}) : _picker = picker ?? ImagePicker();

  @override
  Future<CaptureMediaResult?> pickFromCamera() async {
    final XFile? file = await _picker.pickImage(
      source: ImageSource.camera,
      maxWidth: 2048,
      maxHeight: 2048,
    );
    if (file == null) return null;
    return _resultFromXFile(file);
  }

  @override
  Future<CaptureMediaResult?> pickFromGallery() async {
    final XFile? file = await _picker.pickImage(
      source: ImageSource.gallery,
      maxWidth: 2048,
      maxHeight: 2048,
    );
    if (file == null) return null;
    return _resultFromXFile(file);
  }

  Future<CaptureMediaResult> _resultFromXFile(XFile file) async {
    final bytes = await file.readAsBytes();
    final name = file.name;
    final ext = name.split('.').last.toLowerCase();
    final contentType = _contentTypeFor(ext);
    return CaptureMediaResult(
      bytes: bytes,
      fileName: name,
      contentType: contentType,
    );
  }

  String _contentTypeFor(String ext) {
    switch (ext) {
      case 'jpg':
      case 'jpeg':
        return 'image/jpeg';
      case 'png':
        return 'image/png';
      case 'webp':
        return 'image/webp';
      default:
        return 'image/jpeg';
    }
  }
}
