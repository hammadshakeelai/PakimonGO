import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';
import 'package:mapbox_maps_flutter/mapbox_maps_flutter.dart';

import 'core/auth/auth_service.dart';
import 'core/config/app_config.dart';
import 'core/network/api_client.dart';
import 'features/age_gate/data/shared_prefs_age_gate_store.dart';
import 'features/age_gate/domain/age_gate_service.dart';
import 'features/age_gate/presentation/age_gate.dart';
import 'features/auth/presentation/login_screen.dart';
import 'features/capture/data/capture_repository.dart';
import 'features/capture/presentation/capture_screen.dart';
import 'features/capture/presentation/default_capture_media_service.dart';
import 'features/leaderboard/domain/leaderboard_viewmodel.dart';
import 'features/leaderboard/presentation/leaderboard_screen.dart';
import 'features/map/domain/map_viewmodel.dart';
import 'features/map/presentation/map_screen.dart';
import 'features/notifications/domain/notification_viewmodel.dart';
import 'features/onboarding/data/shared_prefs_onboarding_store.dart';
import 'features/onboarding/domain/onboarding_service.dart';
import 'features/onboarding/presentation/onboarding.dart';
import 'features/notifications/presentation/notification_screen.dart';
import 'features/profile/domain/profile_viewmodel.dart';
import 'features/profile/presentation/profile_screen.dart';
import 'features/submissions/domain/submission_history_viewmodel.dart';
import 'features/submissions/presentation/submission_history_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp();

  if (AppConfig.hasMapboxToken) {
    MapboxOptions.setAccessToken(AppConfig.mapboxAccessToken);
  }

  runApp(PakimonGoApp());
}

class PakimonGoApp extends StatelessWidget {
  PakimonGoApp({super.key});

  final AuthService _authService = AuthService();
  final AgeGateService _ageGate =
      AgeGateService(store: SharedPrefsAgeGateStore());
  final OnboardingService _onboarding =
      OnboardingService(store: SharedPrefsOnboardingStore());

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'PakimonGO',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.green),
        useMaterial3: true,
      ),
      home: AgeGate(
        service: _ageGate,
        child: OnboardingGate(
          service: _onboarding,
          child: _AuthGate(authService: _authService),
        ),
      ),
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

class _HomeScreenState extends State<HomeScreen> with WidgetsBindingObserver {
  int _currentIndex = 0;
  late final MapViewModel _mapViewModel = MapViewModel(
    repository: CaptureRepository(client: widget.apiClient),
  );
  late final SubmissionHistoryViewModel _historyViewModel =
      SubmissionHistoryViewModel(
    repository: CaptureRepository(client: widget.apiClient),
  );
  late final NotificationViewModel _notificationViewModel =
      NotificationViewModel(
    repository: CaptureRepository(client: widget.apiClient),
  );
  late final LeaderboardViewModel _leaderboardViewModel =
      LeaderboardViewModel(
    repository: CaptureRepository(client: widget.apiClient),
  );
  late final ProfileViewModel _profileViewModel = ProfileViewModel(
    repository: CaptureRepository(client: widget.apiClient),
  );

  late final List<Widget> _screens = [
    MapScreen(viewModel: _mapViewModel),
    CaptureScreen(
      mediaService: createDefaultMediaService(),
      repository: CaptureRepository(client: widget.apiClient),
    ),
    SubmissionHistoryScreen(viewModel: _historyViewModel),
    LeaderboardScreen(viewModel: _leaderboardViewModel),
  ];

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);
    _notificationViewModel.fetchUnreadCount();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _notificationViewModel.fetchUnreadCount();
    }
  }

  void _openNotifications() {
    Navigator.of(context).push(
      MaterialPageRoute(
        builder: (_) => NotificationScreen(viewModel: _notificationViewModel),
      ),
    ).then((_) => _notificationViewModel.fetchUnreadCount());
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('PakimonGO'),
        actions: [
          Stack(
            children: [
              IconButton(
                icon: const Icon(Icons.notifications_outlined),
                onPressed: _openNotifications,
              ),
              if (_notificationViewModel.unreadCount > 0)
                Positioned(
                  right: 6,
                  top: 6,
                  child: Container(
                    padding: const EdgeInsets.all(4),
                    decoration: const BoxDecoration(
                      color: Colors.red,
                      shape: BoxShape.circle,
                    ),
                    constraints: const BoxConstraints(
                      minWidth: 18,
                      minHeight: 18,
                    ),
                    child: Text(
                      _notificationViewModel.unreadCount > 99
                          ? '99+'
                          : '${_notificationViewModel.unreadCount}',
                      style: const TextStyle(
                        color: Colors.white,
                        fontSize: 10,
                        fontWeight: FontWeight.bold,
                      ),
                      textAlign: TextAlign.center,
                    ),
                  ),
                ),
            ],
          ),
          IconButton(
            icon: const Icon(Icons.person),
            onPressed: () {
              Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (_) => ProfileScreen(
                    viewModel: _profileViewModel,
                    authService: widget.authService,
                    repository: CaptureRepository(client: widget.apiClient),
                  ),
                ),
              );
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
          NavigationDestination(
              icon: Icon(Icons.history), label: 'History'),
          NavigationDestination(
              icon: Icon(Icons.leaderboard), label: 'Leaderboard'),
        ],
      ),
    );
  }
}
