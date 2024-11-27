import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../logger.dart';

class SessionService {
  final http.Client httpClient;
  final SharedPreferences sharedPreferences;
  final String baseUrl;
  final String credToken;

  SessionService({
    required this.httpClient,
    required this.sharedPreferences,
    required this.baseUrl,
    required this.credToken,
  });

  Future<void> initializeSession() async {
    final storedToken = sharedPreferences.getString('sessionToken');
    final storedSessionExpiredTimestamp =
        sharedPreferences.getInt('sessionExpiredTimestamp');
    final currentTime = DateTime.now().millisecondsSinceEpoch;

    if (storedToken != null &&
        storedSessionExpiredTimestamp != null &&
        storedSessionExpiredTimestamp > currentTime) {
      logger.info('Session token reused.');
      return;
    }

    logger.info('Initializing session');
    final response = await httpClient.post(
      Uri.parse('$baseUrl/v1/sessions'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Basic $credToken'
      },
    );

    logger.info("Response: ${response.statusCode} ${response.body}");

    if (response.statusCode >= 200 || response.statusCode < 300) {
      final decodedBody = json.decode(response.body);
      final token = decodedBody['data']['value'];
      final int expiresInSeconds = decodedBody['data']['expires_in'];

      await sharedPreferences.setString('sessionToken', token);
      await sharedPreferences.setInt(
          'sessionExpiredTimestamp', currentTime + (expiresInSeconds * 1000));
      logger.info('Session initialized and stored.');
    } else {
      logger.severe(
          'Failed to initialize session. Status code: ${response.statusCode}');
      throw Exception('Failed to initialize session');
    }
  }

  Future<String> getSessionToken() async {
    return sharedPreferences.getString('sessionToken') ?? '';
  }
}
