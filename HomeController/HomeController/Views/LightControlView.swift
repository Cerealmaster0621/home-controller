//
//  LightControlView.swift
//  HomeController
//
//  Light Control View
//

import SwiftUI

struct LightControlView: View {
    @State private var isLoading = false
    @State private var alertMessage = ""
    @State private var showAlert = false
    
    private let networkService = NetworkService.shared
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // MARK: - Quick Controls
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Quick Controls")
                            .font(.headline)
                            .foregroundColor(.secondary)
                        
                        HStack(spacing: 12) {
                            LightButton(
                                title: "On",
                                icon: "lightbulb.fill",
                                color: .yellow,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.turnOnLight)
                            }
                            
                            LightButton(
                                title: "Off",
                                icon: "lightbulb.slash",
                                color: .gray,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.turnOffLight)
                            }
                        }
                    }
                    .padding(.horizontal)
                    
                    Divider()
                    
                    // MARK: - Brightness Modes
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Brightness Modes")
                            .font(.headline)
                            .foregroundColor(.secondary)
                        
                        VStack(spacing: 12) {
                            LightButton(
                                title: "All Bright",
                                icon: "sun.max.fill",
                                color: .orange,
                                isFullWidth: true,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.setLightAllBright)
                            }
                            
                            LightButton(
                                title: "Bright",
                                icon: "sun.min.fill",
                                color: .yellow,
                                isFullWidth: true,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.setLightBright)
                            }
                            
                            LightButton(
                                title: "Dark",
                                icon: "moon.fill",
                                color: .indigo,
                                isFullWidth: true,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.setLightDark)
                            }
                        }
                    }
                    .padding(.horizontal)
                    
                    // MARK: - Visual Preview
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Preview")
                            .font(.headline)
                            .foregroundColor(.secondary)
                        
                        ZStack {
                            RoundedRectangle(cornerRadius: 20)
                                .fill(
                                    LinearGradient(
                                        gradient: Gradient(colors: [Color.yellow.opacity(0.3), Color.orange.opacity(0.2)]),
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )
                                .frame(height: 150)
                            
                            VStack {
                                Image(systemName: "lightbulb.fill")
                                    .font(.system(size: 50))
                                    .foregroundColor(.yellow)
                                
                                Text("Light Control")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
            .navigationTitle("Light Control")
            .alert("Message", isPresented: $showAlert) {
                Button("OK", role: .cancel) { }
            } message: {
                Text(alertMessage)
            }
        }
    }
    
    // MARK: - Helper Methods
    
    private func performAction(_ action: @escaping () async throws -> LightResponse) async {
        isLoading = true
        defer { isLoading = false }
        
        do {
            let response = try await action()
            await MainActor.run {
                alertMessage = response.message
                showAlert = true
            }
        } catch {
            await MainActor.run {
                alertMessage = error.localizedDescription
                showAlert = true
            }
        }
    }
}

// MARK: - Light Button Component

struct LightButton: View {
    let title: String
    let icon: String
    var color: Color = .yellow
    var isFullWidth: Bool = false
    var isLoading: Bool = false
    let action: () async -> Void
    
    var body: some View {
        Button {
            Task {
                await action()
            }
        } label: {
            HStack {
                if isFullWidth {
                    Spacer()
                }
                
                Image(systemName: icon)
                    .font(.system(size: 18))
                
                Text(title)
                    .font(.body)
                    .fontWeight(.semibold)
                
                if isFullWidth {
                    Spacer()
                }
            }
            .padding(.vertical, 14)
            .padding(.horizontal, 20)
            .background(color)
            .foregroundColor(.white)
            .cornerRadius(12)
        }
        .disabled(isLoading)
        .opacity(isLoading ? 0.6 : 1.0)
    }
}

#Preview {
    LightControlView()
}

