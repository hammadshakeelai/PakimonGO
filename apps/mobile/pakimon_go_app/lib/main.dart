import 'package:flutter/material.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';

import 'core/auth/auth_service.dart';
import 'core/config/app_config.dart';
import 'core/network/api_client.dart';
import 'features/auth/presentation/login_screen.dart';
import 'features/capture/data/capture_repository.dart';
import 'features/capture/presentation/capture_screen.dart';
import 'features/capture/presentation/default_capture_media_service.dart';
import 'features/map/presentation/map_screen.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  if (AppConfig.hasMapboxToken) {
    MapboxOptions.setAccessToken(AppConfig.mapboxAccessToken);
  }

  runApp(PakimonGoApp());
}

class PakimonGoApp extends StatelessWidget {
  PakimonGoApp({super.key});

  final AuthService _authService = AuthService();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PakimonGO',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: _AuthGate(authService: _authService),
    );
  }
}

class _AuthGate extends StatefulWidget {
  final AuthService authService;

  const _AuthGate({required this.authService});

  @override
  State<_AuthGate> createState() => _AuthGateState();
}

class _AuthGateState extends State<_AuthGate> {
  late ApiClient _apiClient;

  @override
  void initState() {
    super.initState();
    _apiClient = ApiClient(
      tokenProvider: () => widget.authService.effectiveToken,
    );
    widget.authService.addListener(_onAuthChanged);
  }

  @override
  void dispose() {
    widget.authService.removeListener(_onAuthChanged);
    _apiClient.close();
    super.dispose();
  }

  void _onAuthChanged() {
    setState(() {});
  }

  @override
  Widget build(BuildContext context) {
    if (!widget.authService.isAuthenticated) {
      return LoginScreen(
        authService: widget.authService,
        onLoginComplete: () {
          _apiClient = ApiClient(
            tokenProvider: () => widget.authService.effectiveToken,
          );
        },
      );
    }
    return HomeScreen(
      authService: widget.authService,
      apiClient: _apiClient,
    );
  }
}

class HomeScreen extends StatefulWidget {
  final AuthService authService;
  final ApiClient apiClient;

  const HomeScreen({
    super.key,
    required this.authService,
    required this.apiClient,
  });

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int _currentIndex = 0;

  late final List<Widget> _screens = [
    const MapScreen(),
    CaptureScreen(
      mediaService: createDefaultMediaService(),
      repository: CaptureRepository(client: widget.apiClient),
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PakimonGO'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              widget.authService.logout();
            },
          ),
        ],
      ),
      body: _screens[_currentIndex],
      bottomNavigationBar: NavigationBar(
        selectedIndex: _currentIndex,
        onDestinationSelected: (i) => setState(() => _currentIndex = i),
        destinations: const [
          NavigationDestination(icon: Icon(Icons.map), label: 'Map'),
          NavigationDestination(
              icon: Icon(Icons.camera_alt), label: 'Capture'),
        ],
      ),
    );
  }
}
