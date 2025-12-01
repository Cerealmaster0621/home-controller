//
//  ContentView.swift
//  HomeController
//
//  Main view with tab bar navigation
//

import SwiftUI

struct ContentView: View {
    @State private var selectedTab = 0
    
    var body: some View {
        TabView(selection: $selectedTab) {
            ACControlView()
                .tabItem {
                    Label("AC", systemImage: "snowflake")
                }
                .tag(0)
            
            LightControlView()
                .tabItem {
                    Label("Light", systemImage: "lightbulb.fill")
                }
                .tag(1)
            
            SettingsView()
                .tabItem {
                    Label("Settings", systemImage: "gear")
                }
                .tag(2)
        }
        .accentColor(.blue)
    }
}

// MARK: - Settings View

struct SettingsView: View {
    var body: some View {
        NavigationView {
            List {
                Section(header: Text("Backend Configuration")) {
                    HStack {
                        Text("Server URL")
                        Spacer()
                        Text(Config.baseURL)
                            .foregroundColor(.secondary)
                            .font(.caption)
                    }
                }
                
                Section(header: Text("About")) {
                    HStack {
                        Text("App Name")
                        Spacer()
                        Text("Home Controller")
                            .foregroundColor(.secondary)
                    }
                    
                    HStack {
                        Text("Version")
                        Spacer()
                        Text("1.0.0")
                            .foregroundColor(.secondary)
                    }
                }
                
                Section(header: Text("Information")) {
                    VStack(alignment: .leading, spacing: 8) {
                        Text("Configuration")
                            .font(.headline)
                        
                        Text("To change the backend server URL, edit the baseURL in Config.swift")
                            .font(.caption)
                            .foregroundColor(.secondary)
                        
                        Text("Example: http://192.168.1.100:8000")
                            .font(.caption)
                            .foregroundColor(.blue)
                    }
                    .padding(.vertical, 4)
                }
            }
            .navigationTitle("Settings")
        }
    }
}

#Preview {
    ContentView()
}
