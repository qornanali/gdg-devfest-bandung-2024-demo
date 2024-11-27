import 'package:http/http.dart' as http;
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'package:tanya_tanya_app/services/chat_service.dart';
import 'services/session_service.dart';
import 'logger.dart';
import 'pages/chat_page.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await dotenv.load();
  configureLogging();
  SharedPreferences sharedPreferences = await SharedPreferences.getInstance();
  http.Client httpClient = http.Client();
  String baseUrl = dotenv.env['BACKEND_BASE_URL']!;
  SessionService sessionService = SessionService(
    httpClient: httpClient,
    sharedPreferences: sharedPreferences,
    baseUrl: baseUrl,
    credToken: dotenv.env['BACKEND_CREDENTIAL_TOKEN']!,
  );
  ChatService chatService = ChatService(
    httpClient: httpClient,
    sharedPreferences: sharedPreferences,
    baseUrl: baseUrl,
    sessionService: sessionService,
  );
  await sessionService.initializeSession();
  runApp(ChatApp(chatService: chatService));
}

class ChatApp extends StatelessWidget {
  final ChatService chatService;
  const ChatApp({super.key, required this.chatService});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ChatPage(
        chatService: chatService,
      ),
    );
  }
}
