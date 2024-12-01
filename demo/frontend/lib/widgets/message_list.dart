import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

class MessageList extends StatelessWidget {
  final List<Map<String, dynamic>> messages;

  const MessageList({Key? key, required this.messages}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: ListView.builder(
        itemCount: messages.length,
        itemBuilder: (context, index) {
          final message = messages[index];
          final sender = message['sender'];
          final text = message['text'];
          final createdTime = message['created_time'];
          final isSentByUser = sender == 'You';

          if (isSentByUser) {
            return Align(
              alignment: Alignment.centerRight,
              child: Container(
                margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
                padding: const EdgeInsets.all(8),
                decoration: BoxDecoration(
                  color: Colors.blue[300],
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      '${sender}',
                      style: const TextStyle(fontSize: 12),
                    ),
                    Text(
                      '${text}',
                      style: const TextStyle(fontSize: 16),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      DateFormat('hh:mm a, dd MMM yyyy').format(
                          DateTime.fromMillisecondsSinceEpoch(createdTime!)),
                      style: TextStyle(
                        fontSize: 10,
                        color: Colors.grey[600],
                      ),
                    ),
                  ],
                ),
              ),
            );
          }

          return Align(
            alignment: Alignment.centerLeft,
            child: Container(
              margin: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: Colors.blue[100],
                borderRadius: BorderRadius.circular(8),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    '${sender}',
                    style: const TextStyle(fontSize: 12),
                  ),
                  Text(
                    '${text}',
                    style: const TextStyle(fontSize: 16),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    DateFormat('hh:mm a, dd MMM yyyy').format(
                        DateTime.fromMillisecondsSinceEpoch(createdTime!)),
                    style: TextStyle(
                      fontSize: 10,
                      color: Colors.grey[600],
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
