from database import TicketDatabase


class TicketManager:
    def __init__(self):
        self.db = TicketDatabase()

    def create_ticket(self, name, email, issue, priority="Medium"):
        """
        Create a new support ticket.
        """
        self.db.add_ticket(
            name=name,
            email=email,
            issue=issue,
            priority=priority
        )

        return {
            "success": True,
            "message": "Support ticket created successfully."
        }

    def list_tickets(self):
        """
        Return all support tickets.
        """
        return self.db.get_all_tickets()

    def get_ticket(self, ticket_id):
        """
        Return a ticket by ID.
        """
        ticket = self.db.get_ticket(ticket_id)

        if ticket:
            return ticket

        return {
            "success": False,
            "message": "Ticket not found."
        }

    def update_ticket_status(self, ticket_id, status):
        """
        Update the status of a ticket.
        """

        valid_status = [
            "Open",
            "In Progress",
            "Resolved",
            "Closed"
        ]

        if status not in valid_status:
            return {
                "success": False,
                "message": "Invalid status."
            }

        ticket = self.db.get_ticket(ticket_id)

        if not ticket:
            return {
                "success": False,
                "message": "Ticket not found."
            }

        self.db.update_status(ticket_id, status)

        return {
            "success": True,
            "message": f"Ticket #{ticket_id} updated to '{status}'."
        }

    def delete_ticket(self, ticket_id):
        """
        Delete a ticket.
        """

        ticket = self.db.get_ticket(ticket_id)

        if not ticket:
            return {
                "success": False,
                "message": "Ticket not found."
            }

        self.db.delete_ticket(ticket_id)

        return {
            "success": True,
            "message": "Ticket deleted successfully."
        }

    def search_ticket(self, keyword):
        """
        Search tickets by keyword.
        """
        return self.db.search_tickets(keyword)
