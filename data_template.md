## Database Design
- **Patients**: Demographics, contact information, preferences
- **Providers**: Healthcare professionals, specialties, credentials
- **Care Plans**: Treatment plans, goals, timelines
- **Care Teams**: Provider relationships, roles, responsibilities
- **Communications**: Messages, alerts, notifications
- **Appointments**: Scheduling, telemedicine sessions
- **Documents**: Medical records, care notes, reports

### Relationships
- Patient → Care Teams (Many-to-Many)
- Care Plans → Care Activities (One-to-Many)
- Providers → Specialties (Many-to-Many)
- Communications → Care Teams (Many-to-Many)
