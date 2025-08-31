// ContentView.swift

import SwiftUI

struct ContentView: View {
    // State Variables
    @State private var messageText: String = ""
    @State private var messages: [String] = ["Ask me about healthcare or fashion!"]

    // Create an instance of our API service
    private let apiService = APIService()

    var body: some View {
        ZStack {
            Color("AppBackgroundCordovan").ignoresSafeArea()
            
            VStack {
                Text("AI Chatbot")
                    .font(.largeTitle)
                    .fontWeight(.bold)
                    .foregroundColor(Color("AccentColor"))
                    .padding(.top)

                ScrollView {
                    VStack(alignment: .leading, spacing: 10) {
                        ForEach(messages, id: \.self) { message in
                            if message.starts(with: "You:") {
                                Text(message)
                                    .padding(12)
                                    .background(Color("User"))
                                    .foregroundColor(.white)
                                    .cornerRadius(10)
                                    .frame(maxWidth: .infinity, alignment: .trailing)
                            } else {
                                Text(message)
                                    .padding(12)
                                    .background(Color("Chat"))
                                    .foregroundColor(Color("Text"))
                                    .cornerRadius(10)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                            }
                        }
                    }
                    .padding()
                }

                Spacer()

                Divider()

                HStack {
                    TextField("Type your message...", text: $messageText)
                        .textFieldStyle(RoundedBorderTextFieldStyle())
                        .padding(.leading)

                    Button(action: {
                        Task {
                            await sendMessage()
                        }
                    }) {
                        Image(systemName: "paperplane.fill")
                            .font(.title2)
                            .foregroundColor(Color("accent"))
                    }
                    .padding(.horizontal)
                    // --- FIX: Add this line to prioritize the button's space ---
                    .layoutPriority(1)
                }
                .padding(.bottom)
            }
        }
    }
    
    func sendMessage() async {
        let userMessage = messageText
        if userMessage.isEmpty { return }
        
        messages.append("You: \(userMessage)")
        self.messageText = ""
        
        do {
            let botResponse = try await apiService.sendMessage(message: userMessage)
            messages.append(botResponse)
        } catch {
            messages.append("Error: \(error.localizedDescription)")
        }
    }
}

#Preview {
    ContentView()
}
 
