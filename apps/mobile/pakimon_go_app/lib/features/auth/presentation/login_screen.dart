import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';
import 'package:google_sign_in/google_sign_in.dart';

import '../../../core/auth/auth_service.dart';
import '../../../core/network/api_client.dart';
import '../../capture/data/capture_repository.dart';

// Web OAuth client ID from google-services.json (public identifier, not a secret).
const _googleServerClientId =
    '156483222458-6j6kh0nc7vm0gd781vtgpk2f5hb69ghn.apps.googleusercontent.com';

class LoginScreen extends StatefulWidget {
  final AuthService authService;
  final void Function()? onLoginComplete;

  const LoginScreen({
    super.key,
    required this.authService,
    this.onLoginComplete,
  });

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _userIdCtrl = TextEditingController(text: 'alice');
  final _tokenCtrl = TextEditingController();
  bool _useToken = false;
  bool _gsiInitialized = false;
  String _status = '';
  bool _loading = false;

  Future<void> _login() async {
    setState(() {
      _loading = true;
      _status = '';
    });

    try {
      if (_useToken) {
        widget.authService.loginWithToken(_tokenCtrl.text.trim());
      } else {
        widget.authService.loginWithUserId(_userIdCtrl.text.trim());
      }

      final repo = CaptureRepository(
        client: ApiClient(
          tokenProvider: () => widget.authService.effectiveToken,
        ),
      );
      await repo.getProfile();

      if (mounted) {
        setState(() => _status = 'Logged in');
        widget.onLoginComplete?.call();
      }
    } on ApiException catch (e) {
      setState(() => _status = 'API error: ${e.message}');
    } catch (e) {
      setState(() => _status = 'Connection error: $e');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _googleLogin() async {
    setState(() {
      _loading = true;
      _status = '';
    });
    try {
      if (!_gsiInitialized) {
        await GoogleSignIn.instance.initialize(
          serverClientId: _googleServerClientId,
        );
        _gsiInitialized = true;
      }
      final account = await GoogleSignIn.instance.authenticate();
      final idToken = account.authentication.idToken;
      if (idToken == null) {
        throw Exception('Google did not return an ID token');
      }
      final userCred = await FirebaseAuth.instance.signInWithCredential(
        GoogleAuthProvider.credential(idToken: idToken),
      );
      final firebaseUser = userCred.user;
      final firebaseIdToken = await firebaseUser?.getIdToken();
      if (firebaseUser == null || firebaseIdToken == null) {
        throw Exception('Firebase did not return an ID token');
      }
      // Register a refresher: Firebase ID tokens expire after ~1 hour, so
      // every API call pulls a currently-valid token from the SDK cache.
      widget.authService.loginWithToken(
        firebaseIdToken,
        refresher: () => firebaseUser.getIdToken(),
      );

      final repo = CaptureRepository(
        client: ApiClient(
          tokenProvider: () => widget.authService.effectiveToken,
        ),
      );
      await repo.getProfile();

      if (mounted) {
        setState(() => _status = 'Signed in with Google');
        widget.onLoginComplete?.call();
      }
    } on ApiException catch (e) {
      setState(() => _status = 'API error: ${e.message}');
    } catch (e) {
      setState(() => _status = 'Google sign-in failed: $e');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  void dispose() {
    _userIdCtrl.dispose();
    _tokenCtrl.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('PakimonGO Login')),
      body: Padding(
        padding: const EdgeInsets.all(24),
        child: SingleChildScrollView(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Icon(Icons.pets, size: 80, color: Colors.green),
              const SizedBox(height: 16),
              Text(
                'PakimonGO',
                style: Theme.of(context).textTheme.headlineMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 8),
              Text(
                'Sign in to start capturing wildlife',
                style: Theme.of(context).textTheme.bodyMedium,
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              if (!_useToken) ...[
                TextField(
                  controller: _userIdCtrl,
                  decoration: const InputDecoration(
                    labelText: 'User ID',
                    hintText: 'Enter your user ID (e.g. alice)',
                    prefixIcon: Icon(Icons.person),
                    border: OutlineInputBorder(),
                  ),
                ),
              ] else ...[
                TextField(
                  controller: _tokenCtrl,
                  decoration: const InputDecoration(
                    labelText: 'Auth Token',
                    hintText: 'Paste your auth token',
                    prefixIcon: Icon(Icons.key),
                    border: OutlineInputBorder(),
                  ),
                ),
              ],
              const SizedBox(height: 8),
              TextButton(
                onPressed: () => setState(() => _useToken = !_useToken),
                child: Text(
                  _useToken
                      ? 'Use User ID instead'
                      : 'Paste auth token instead',
                ),
              ),
              const SizedBox(height: 16),
              ElevatedButton.icon(
                onPressed: _loading ? null : _login,
                icon: _loading
                    ? const SizedBox(
                        width: 18,
                        height: 18,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Icon(Icons.login),
                label: Text(_loading ? 'Signing in...' : 'Sign In'),
              ),
              const SizedBox(height: 12),
              const Row(
                children: [
                  Expanded(child: Divider()),
                  Padding(
                    padding: EdgeInsets.symmetric(horizontal: 8),
                    child: Text('or'),
                  ),
                  Expanded(child: Divider()),
                ],
              ),
              const SizedBox(height: 12),
              OutlinedButton.icon(
                onPressed: _loading ? null : _googleLogin,
                icon: const Icon(Icons.account_circle),
                label: const Text('Sign in with Google'),
              ),
              if (_status.isNotEmpty) ...[
                const SizedBox(height: 16),
                Card(
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Text(_status),
                  ),
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
