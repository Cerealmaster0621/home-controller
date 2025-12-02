//
//  ACControlView.swift
//  HomeController
//
//  Air Conditioner Control View
//

import SwiftUI

struct ACControlView: View {
    @State private var isLoading = false
    @State private var alertMessage = ""
    @State private var showAlert = false
    
    private let networkService = NetworkService.shared
    
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 24) {
                    // MARK: - Mode Controls
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Mode")
                            .font(.headline)
                            .foregroundColor(.secondary)
                        
                        HStack(spacing: 12) {
                            ControlButton(
                                title: "Aircon",
                                icon: "snowflake",
                                color: .blue,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.turnOnAircon)
                            }
                            
                            ControlButton(
                                title: "Heater",
                                icon: "flame.fill",
                                color: .orange,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.turnOnHeater)
                            }
                            
                            ControlButton(
                                title: "Off",
                                icon: "power",
                                color: .gray,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.turnOffAC)
                            }
                        }
                    }
                    .padding(.horizontal)
                    
                    Divider()
                    
                    // MARK: - Temperature Controls
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Temperature")
                            .font(.headline)
                            .foregroundColor(.secondary)
                        
                        VStack(spacing: 12) {
                            // Aircon Temperature
                            HStack {
                                Text("Aircon")
                                    .frame(width: 80, alignment: .leading)
                                
                                Spacer()
                                
                                ControlButton(
                                    title: "Temp Up",
                                    icon: "chevron.up",
                                    color: .blue,
                                    isCompact: true,
                                    isLoading: isLoading
                                ) {
                                    await performAction(networkService.increaseAirconTemp)
                                }
                            }
                            
                            // Heater Temperature
                            HStack {
                                Text("Heater")
                                    .frame(width: 80, alignment: .leading)
                                
                                Spacer()
                                
                                ControlButton(
                                    title: "Temp Up",
                                    icon: "chevron.up",
                                    color: .orange,
                                    isCompact: true,
                                    isLoading: isLoading
                                ) {
                                    await performAction(networkService.increaseHeaterTemp)
                                }
                                
                                ControlButton(
                                    title: "Temp Down",
                                    icon: "chevron.down",
                                    color: .orange,
                                    isCompact: true,
                                    isLoading: isLoading
                                ) {
                                    await performAction(networkService.decreaseHeaterTemp)
                                }
                            }
                        }
                    }
                    .padding(.horizontal)
                    
                    Divider()
                    
                    // MARK: - Timer Controls
                    VStack(alignment: .leading, spacing: 12) {
                        Text("Timer")
                            .font(.headline)
                            .foregroundColor(.secondary)
                        
                        HStack(spacing: 12) {
                            ControlButton(
                                title: "On",
                                icon: "timer",
                                color: .purple,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.turnOnTimer)
                            }
                            
                            ControlButton(
                                title: "Increase",
                                icon: "plus",
                                color: .purple,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.increaseTimer)
                            }
                            
                            ControlButton(
                                title: "Decrease",
                                icon: "minus",
                                color: .purple,
                                isLoading: isLoading
                            ) {
                                await performAction(networkService.decreaseTimer)
                            }
                        }
                    }
                    .padding(.horizontal)
                }
                .padding(.vertical)
            }
            .navigationTitle("AC Control")
            .alert("Message", isPresented: $showAlert) {
                Button("OK", role: .cancel) { }
            } message: {
                Text(alertMessage)
            }
        }
    }
    
    // MARK: - Helper Methods
    
    private func performAction(_ action: @escaping () async throws -> ACResponse) async {
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

// MARK: - Control Button Component

struct ControlButton: View {
    let title: String
    let icon: String
    var color: Color = .blue
    var isCompact: Bool = false
    var isLoading: Bool = false
    let action: () async -> Void
    
    var body: some View {
        Button {
            Task {
                await action()
            }
        } label: {
            HStack {
                if !isCompact {
                    Spacer()
                }
                
                Image(systemName: icon)
                    .font(.system(size: isCompact ? 14 : 16))
                
                Text(title)
                    .font(isCompact ? .footnote : .body)
                    .fontWeight(.semibold)
                
                if !isCompact {
                    Spacer()
                }
            }
            .padding(.vertical, isCompact ? 8 : 12)
            .padding(.horizontal, isCompact ? 12 : 16)
            .background(color)
            .foregroundColor(.white)
            .cornerRadius(10)
        }
        .disabled(isLoading)
        .opacity(isLoading ? 0.6 : 1.0)
    }
}

#Preview {
    ACControlView()
}

