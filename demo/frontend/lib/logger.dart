import 'package:logging/logging.dart';

final Logger logger = Logger('AppLogger');

void configureLogging() {
  Logger.root.level = Level.ALL;

  Logger.root.onRecord.listen((LogRecord record) {
    print(
        '[${record.level.name}] ${record.time}: ${record.loggerName} - ${record.message}');
    if (record.error != null) {
      print('Error: ${record.error}');
    }
    if (record.stackTrace != null) {
      print('Stacktrace: ${record.stackTrace}');
    }
  });
}
