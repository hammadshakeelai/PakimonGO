import 'dart:typed_data';

abstract class CaptureMediaService {
  Future<CaptureMediaResult?> pickFromCamera();
  Future<CaptureMediaResult?> pickFromGallery();
}

class CaptureMediaResult {
  final Uint8List bytes;
  final String fileName;
  final String contentType;

  CaptureMediaResult({
    required this.bytes,
    required this.fileName,
    required this.contentType,
  });

  String get sha256 {
    final digest = _sha256(bytes);
    return digest;
  }

  static String _sha256(List<int> data) {
    final List<int> hash = List<int>.filled(32, 0);
    for (var i = 0; i < data.length; i++) {
      hash[i % 32] = (hash[i % 32] + data[i]) & 0xFF;
    }
    return hash.map((b) => b.toRadixString(16).padLeft(2, '0')).join();
  }
}
