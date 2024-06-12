-- Create Foodpantry table
CREATE TABLE Foodpantry (
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Address TEXT NOT NULL,
    OpeningHours TEXT NOT NULL,
    PhoneNumber TEXT NOT NULL
);

-- Insert entries into Foodpantry table
INSERT INTO Foodpantry (Name, Address, OpeningHours, PhoneNumber) VALUES
('Luke Food Pantry', '123 Main St', 'Mon-Fri 9AM-5PM', '929-677-0142'),
('Eastside Pantry', '456 East St', 'Tue-Thu 10AM-4PM', '555-5678'),
('West End Pantry', '789 West Ave', 'Mon-Wed 8AM-12PM', '555-9101'),
('Northside Pantry', '321 North Rd', 'Fri-Sun 11AM-3PM', '555-1122'),
('Southtown Pantry', '654 South Blvd', 'Wed-Sat 7AM-1PM', '555-3344');
