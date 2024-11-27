import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../logger.dart';
import 'session_service.dart';

class ChatService {
  final http.Client httpClient;
  final SharedPreferences sharedPreferences;
  final String baseUrl;
  final SessionService sessionService;

  ChatService({
    required this.httpClient,
    required this.sharedPreferences,
    required this.baseUrl,
    required this.sessionService,
  });

  Future<Map<String, dynamic>> sendMessage(String message) async {
    final token = await sessionService.getSessionToken();
    logger.info('Sending message: $message');
    final response = await httpClient.post(
      Uri.parse('$baseUrl/v1/chat'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: json.encode({'message': message}),
    );

    logger.info("Response: ${response.statusCode} ${response.body}");

    if (response.statusCode >= 200 && response.statusCode < 300) {
      final data = json.decode(response.body);
      if (data['success'] == true) {
        return data['data'];
      } else {
        logger.severe('Chat message failed. Response: ${response.body}');
        throw Exception('Failed to send chat message');
      }
    } else if (response.statusCode == 401) {
      logger.info('Session expired. Reinitializing session...');
      await sessionService.initializeSession();
      return await sendMessage(message);
    } else {
      logger.severe(
          'Failed to send message. Status code: ${response.statusCode}');
      throw Exception('Failed to send chat message');
    }
  }
}
