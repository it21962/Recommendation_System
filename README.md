# Αναφορά Υλοποίησης Recommendation System

## 1.Εκκίνηση Υλοποίησης: Random Generator
Η αρχική προσέγγιση ήταν να υλοποιηθεί ένας απλός generator που επιστρέφει τυχαίες προτάσεις.

- Δοκιμάστηκε μέσω Postman.
- Endpoint: `POST /recommendations`
- Σκοπός: να ελεγχθεί η βασική λειτουργία POST/GET request.

## 2.Frequent Generator
Ο πρώτος «έξυπνος» αλγόριθμος.

- Εντοπίζει το πιο πρόσφατο κουπόνι ενός χρήστη.
- Εντοπίζει events που ταιριάζουν με το sport/league του κουπονιού.
- Βασίζεται αρχικά σε CSV αρχεία (`users.csv`, `coupons.csv`, `events.csv`).

## 3.Inference Generator (Dynamic με config)
Ο τελικός recommendation engine.

- Αναλύει τα τελευταία κουπόνια του χρήστη (τελευταίων 30 ημερών).
- Υπολογίζει τα πιο συχνά ζεύγη sport/league.
- Υπολογίζει το μέσο stake ανά ζεύγος.
- Επιστρέφει personalized συστάσεις.

### Ρυθμίσεις μέσω `/config`
- `GET /config`: Επιστρέφει schema εμφάνισης.
- `POST /config`: Επιτρέπει custom schema per company (αποθηκεύεται σε MySQL).

## 4.Unit Testing
Καλύφθηκαν:
- Recommendation logic (inference_generator)
- API endpoints (GET/POST recommendations, GET/POST config)
- Database insertions
- Validation (Pydantic, Marshmallow)

**Coverage:** 98%

## 5.RabbitMQ Integration
### Queues:
- `coupons_queue`
- `events_queue`
- `users_queue`

### Consumers:
- Διαβάζουν από RabbitMQ.
- Επεξεργάζονται τα μηνύματα (single/batch).
- Αποθηκεύουν σε MySQL αν δεν υπάρχει εγγραφή.
- Αν ήδη υπάρχουν τα στοιχεία, απορρίπτει την εισαγωγή τους (έλεγχος διπλότυπων)
- Για κουπόνια: δημιουργούνται recommendations real-time.

## 6.Βάση Δεδομένων (MySQL)
**Χρησιμοποιούνται οι εξής πίνακες:**

| Πίνακας             | Περιγραφή                              |
|---------------------|------------------------------------------|
| `coupons`           | Στοιχεία στοιχημάτων                     |
| `events`            | Επερχόμενα γεγονότα                      |
| `novibet_users`     | Χρήστες Novibet                         |
| `stoiximan_users`   | Χρήστες Stoiximan                       |
| `company_configs`   | Custom schemas ανά εταιρεία             |

## 7.Περιβάλλον
- **Python** 3.11+
- **Flask**, **Pydantic**, **Marshmallow**
- **MySQL** 8
- **RabbitMQ** 3.13.7
- **VS Code**, **GitHub**

## Συμπέρασμα
Το σύστημα:

- Παράγει real-time συστάσεις.
- Διαχειρίζεται εισερχόμενα δεδομένα από queues.
- Έχει πλήρως παραμετροποιήσιμα schemas.

