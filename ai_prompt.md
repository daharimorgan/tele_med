# AI Coding Tool Prompt: Patient Care Coordination & Telemedicine Platform

## ¯ Project Request
Create a **Patient Care Coordination & Telemedicine Platform** (CareConnect Pro) - a comprehensive healthcare application that unifies patient care management, enables real-time care team communication, and provides telemedicine capabilities.

## ‹ Core Application Requirements

### **Primary User Roles:**
1. **Patients** - Access health records, communicate with care team, manage appointments
2. **Healthcare Providers** - Manage patient care, collaborate with care teams, conduct telemedicine sessions  
3. **Care Coordinators** - Orchestrate care across providers, manage care plans, track care gaps
4. **Family Members** - Authorized access to patient information, participate in care decisions

### **Essential Features to Implement:**

#### 1. **Authentication & Authorization System**
- Multi-factor authentication for all user types
- Role-based access control (RBAC) with granular permissions
- HIPAA-compliant session management
- Patient consent management for data sharing

#### 2. **Care Team Communication Hub**
- Real-time secure messaging system between care team members
- HIPAA-compliant chat with message encryption
- File sharing capabilities for medical documents
- Care handoff management with structured transfer protocols
- Notification system for critical patient updates

#### 3. **Patient Data Management**
- Unified patient dashboard consolidating health records from multiple sources
- Interactive care timeline visualization showing patient health journey
- Secure document storage and management system
- Care plan creation, modification, and tracking
- Integration APIs for EHR systems using HL7 FHIR standards

#### 4. **Telemedicine Integration**
- Video consultation platform with screen sharing
- Appointment scheduling system with provider availability
- Pre-consultation questionnaires and health assessments
- Session recording and documentation (with consent)
- Integration with existing healthcare scheduling systems

#### 5. **Care Coordination Automation**
- Workflow engine for automated care processes
- AI-powered care gap identification system
- Task management and assignment system for care teams
- Automated alerts for care milestones and critical events
- Care plan recommendations based on patient data

#### 6. **Patient Portal**
- Personal health record access with complete medical history
- Family member access controls with configurable sharing permissions
- Self-assessment tools and patient-reported outcome measures
- Medication tracking and reminder system
- Direct communication channels with care providers

## ðŸ—ï¸ Technical Architecture Requirements

### **Frontend Development (React.js + TypeScript)**
```typescript
// Core Application Structure
src/
â”œâ”€â”€ components/
â”‚   â”œâ”€â”€ auth/           // Authentication components
â”‚   â”œâ”€â”€ dashboard/      // User dashboards (patient, provider, coordinator)
â”‚   â”œâ”€â”€ messaging/      // Real-time chat and communication
â”‚   â”œâ”€â”€ telemedicine/   // Video consultation interface
â”‚   â”œâ”€â”€ care-plans/     // Care plan management
â”‚   â””â”€â”€ shared/         // Reusable UI components
â”œâ”€â”€ services/
â”‚   â”œâ”€â”€ api/           // API service layer
â”‚   â”œâ”€â”€ auth/          // Authentication services
â”‚   â”œâ”€â”€ websocket/     // Real-time communication
â”‚   â””â”€â”€ integration/   // EHR/external system integration
â”œâ”€â”€ store/             // State management (Redux/Zustand)
â”œâ”€â”€ utils/             // Utility functions and helpers
â””â”€â”€ types/             // TypeScript type definitions
```

### **Backend Development (Node.js + Express.js)**
```javascript
// Microservices Architecture
services/
â”œâ”€â”€ auth-service/          // Authentication and authorization
â”œâ”€â”€ patient-service/       // Patient data management
â”œâ”€â”€ provider-service/      // Healthcare provider management
â”œâ”€â”€ messaging-service/     // Real-time communication
â”œâ”€â”€ telemedicine-service/  // Video consultation management
â”œâ”€â”€ care-coordination/     // Care workflow automation
â”œâ”€â”€ integration-service/   // EHR and external system integration
â””â”€â”€ notification-service/  // Alert and notification management

// Core API Endpoints Structure
/api/v1/
â”œâ”€â”€ /auth              // Authentication endpoints
â”œâ”€â”€ /patients          // Patient management
â”œâ”€â”€ /providers         // Provider management
â”œâ”€â”€ /care-teams        // Care team operations
â”œâ”€â”€ /messaging         // Secure messaging
â”œâ”€â”€ /appointments      // Appointment scheduling
â”œâ”€â”€ /telemedicine      // Video consultation
â”œâ”€â”€ /care-plans        // Care plan management
â”œâ”€â”€ /documents         // Document management
â””â”€â”€ /notifications     // Alert system
```

### **Database Schema (PostgreSQL)**
```sql
-- Core Tables to Implement
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    role user_role NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE patients (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    demographics JSONB,
    emergency_contacts JSONB,
    insurance_info JSONB
);

CREATE TABLE providers (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    specialties TEXT[],
    credentials JSONB,
    npi_number VARCHAR(10)
);

CREATE TABLE care_teams (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    primary_provider_id UUID REFERENCES providers(id),
    team_members JSONB
);

CREATE TABLE care_plans (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    created_by UUID REFERENCES providers(id),
    plan_data JSONB,
    status care_plan_status
);

CREATE TABLE messages (
    id UUID PRIMARY KEY,
    sender_id UUID REFERENCES users(id),
    care_team_id UUID REFERENCES care_teams(id),
    content TEXT,
    message_type message_type,
    encrypted_content BYTEA
);

CREATE TABLE appointments (
    id UUID PRIMARY KEY,
    patient_id UUID REFERENCES patients(id),
    provider_id UUID REFERENCES providers(id),
    appointment_type appointment_type,
    scheduled_time TIMESTAMP,
    status appointment_status
);
```

### **Real-Time Communication (Socket.io)**
```javascript
// WebSocket Event Handlers
const socketEvents = {
    // Care team messaging
    'join_care_team': (careTeamId) => {},
    'send_message': (message) => {},
    'message_received': (message) => {},
    
    // Care coordination alerts
    'care_alert': (alert) => {},
    'care_plan_updated': (update) => {},
    'task_assigned': (task) => {},
    
    // Telemedicine events
    'video_call_initiated': (callData) => {},
    'call_participant_joined': (participant) => {},
    'call_ended': (summary) => {}
};
```

## ðŸ” Security & Compliance Implementation

### **HIPAA Compliance Requirements:**
```javascript
// Security Configuration
const securityConfig = {
    encryption: {
        algorithm: 'AES-256-GCM',
        keyRotation: '90days',
        dataAtRest: true,
        dataInTransit: true
    },
    authentication: {
        mfa: true,
        sessionTimeout: '30minutes',
        passwordPolicy: 'strong',
        auditLogging: true
    },
    dataAccess: {
        roleBasedAccess: true,
        patientConsent: true,
        auditTrail: true,
        dataMinimization: true
    }
};
```

### **AWS Infrastructure Setup:**
```yaml
# AWS Services Configuration
aws_services:
  compute:
    - AWS Lambda (serverless functions)
    - ECS Fargate (containerized services)
  storage:
    - Amazon S3 (document storage)
    - Amazon RDS (PostgreSQL database)
  communication:
    - Amazon Chime SDK (video consultations)
    - Amazon SNS (notifications)
  integration:
    - API Gateway (API management)
    - EventBridge (workflow orchestration)
  security:
    - AWS KMS (encryption keys)
    - AWS IAM (access management)
    - AWS WAF (web application firewall)
```

## ðŸ“± Mobile Application Requirements

### **React Native Implementation:**
```typescript
// Mobile App Structure
mobile/
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ screens/
â”‚   â”‚   â”œâ”€â”€ auth/           // Login, registration
â”‚   â”‚   â”œâ”€â”€ dashboard/      // User-specific dashboards  
â”‚   â”‚   â”œâ”€â”€ messaging/      // Chat and communication
â”‚   â”‚   â”œâ”€â”€ appointments/   // Appointment management
â”‚   â”‚   â”œâ”€â”€ health-records/ // Medical record access
â”‚   â”‚   â””â”€â”€ telemedicine/   // Video consultation
â”‚   â”œâ”€â”€ navigation/         // App navigation structure
â”‚   â”œâ”€â”€ services/          // API and backend services
â”‚   â””â”€â”€ components/        // Reusable mobile components
```

## ðŸ”„ Integration Requirements

### **EHR System Integration (HL7 FHIR):**
```javascript
// FHIR Resource Integration
const fhirResources = {
    Patient: 'Demographics and basic patient information',
    Practitioner: 'Healthcare provider information',
    Encounter: 'Care encounters and visits',
    Observation: 'Clinical observations and measurements',
    CarePlan: 'Treatment and care plans',
    Medication: 'Medication lists and prescriptions',
    DiagnosticReport: 'Lab results and diagnostic reports'
};
```

## ðŸŽ¯ Development Phases & Deliverables

### **Phase 1 MVP (Weeks 1-16):**
- User authentication and role management
- Basic care team messaging
- Patient portal with health record viewing
- Simple appointment scheduling
- Document upload and sharing
- Basic care plan creation

### **Phase 2 Enhanced (Weeks 17-32):**  
- Telemedicine video consultation integration
- Automated care coordination workflows
- Advanced messaging with file sharing
- Family member access portal
- Care gap identification system
- Mobile application development

### **Phase 3 Advanced (Weeks 33-48):**
- AI-powered care recommendations
- Advanced analytics and reporting
- Multi-EHR system integration
- Population health management features
- Third-party API integrations
- Performance optimization and scaling

## ðŸ“Š Testing & Quality Assurance

### **Testing Requirements:**
```javascript
// Testing Strategy
const testingApproach = {
    unit: 'Jest for individual component testing',
    integration: 'API endpoint and service integration testing',
    e2e: 'Cypress for end-to-end user workflow testing',
    security: 'HIPAA compliance and penetration testing',
    performance: 'Load testing for scalability validation',
    accessibility: 'WCAG 2.1 AA compliance testing'
};
```

## ðŸš€ Deployment & DevOps

### **CI/CD Pipeline:**
```yaml
# GitHub Actions Workflow
name: Deploy CareConnect Pro
on: [push]
jobs:
  test:
    - Run unit tests
    - Run integration tests
    - Security scanning
  build:
    - Build Docker containers
    - Push to ECR registry
  deploy:
    - Deploy to AWS ECS
    - Run health checks
    - Update load balancer
```

## ðŸ’¡ Key Success Criteria

1. **Security First**: All patient data must be HIPAA compliant with end-to-end encryption
2. **User Experience**: Intuitive interfaces for all user types with minimal learning curve
3. **Integration**: Seamless connection with existing healthcare systems and EHRs
4. **Scalability**: Architecture must support thousands of concurrent users
5. **Reliability**: 99.9% uptime with robust error handling and recovery
6. **Performance**: Sub-200ms API response times and real-time messaging

## ðŸŽ¯ Immediate Next Steps for AI Coding Tool

1. **Start with authentication system** - Implement secure user registration, login, and role-based access
2. **Create core database models** - Set up PostgreSQL schemas for users, patients, providers, and care teams  
3. **Build basic API endpoints** - Implement REST APIs for user management and basic CRUD operations
4. **Implement secure messaging** - Create real-time chat system with encryption
5. **Design responsive UI components** - Build reusable React components for different user dashboards
6. **Set up AWS infrastructure** - Configure basic cloud services for development environment

**Priority Order**: Authentication â†’ Database â†’ Core APIs â†’ Real-time Messaging â†’ User Interfaces â†’ Telemedicine Integration â†’ Care Coordination Workflows