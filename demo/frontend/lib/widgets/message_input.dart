import 'package:flutter/material.dart';

class MessageInput extends StatelessWidget {
  final TextEditingController controller;
  final Function(String) onSend;

  const MessageInput({Key? key, required this.controller, required this.onSend})
      : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Row(
        children: [
          Expanded(
            child: TextField(
              controller: controller,
              decoration: const InputDecoration(
                border: OutlineInputBorder(),
                hintText: 'Type your message...',
              ),
            ),
          ),
          const SizedBox(width: 8),
          ElevatedButton(
            onPressed: () {
              if (controller.text.isNotEmpty) {
                onSend(controller.text);
              }
            },
            child: const Text('Send'),
          ),
        ],
      ),
    );
  }
}
