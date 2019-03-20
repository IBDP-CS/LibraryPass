# Practice-IA

The collaborative practice IA project.


## Planning

- Users able to login, and backend differentiates students from teachers
- A student can be in 4 states: in dorm, awaiting approval, approved and going to library, checked in to the library, checked out and going back to dorm.

### Student End

- Button to send request to go to the library
- ‘Awaiting approval’ page

## All Teachers

- List of students in the library, going to library, and coming back to the dorm

### House Teacher End

- List of students awaiting for approval with ‘Approve’ and ‘Disapprove’ buttons
- List of students coming back from the library with ‘Check in’ buttons (and time)

### Library Teacher End

- List of students approved and coming to the library with ‘Check in’ buttons (and time)
- List of students checked in and current in the library with ‘Check out’ buttons (and time)

### Process (from a student's perspective)
1. Student requests to go to the library
2. Student approaches teacher (or not?) and the teacher approves the request
3. Student goes to the library
4. Student checks in by the librarian
5. Student studies
6. Student checks out by the librarian
7. Student leaves the library and goes back to the dorm
8. Student checks in by the dorm staff members
9. Done :)


## Questions

- How can we make the process more convenient and quick?


## Stakeholders

- Students: G House Boys (currently)
- Teachers: HM, tutors, library staff
- SLO: Dean of SLO


## Collaboration

- **David Xu**: Front-end webpage interface and interactions
- **Uriah Wu**: Front-end user interaction logic
- **Eric Zhang**: Front-end webpage interface
- **Ben Zhang**: Back-end database
- **George Yu**: Back-end API
