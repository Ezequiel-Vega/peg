from .interface_calculator import ICalculator
from app.team_leader.forms import Headline

class HeadlineCalculator(ICalculator):
    """
        Calculador de resultado Titular
    """
    def __init__(self, form: Headline) -> None:
        self.data = {
                'salute': {
                    'identity_holder': form.identity_holder.data,
                    'presentation': form.presentation.data,
                    'presentation_company': form.presentation_company.data,
                    'debt_presentation': form.debt_presentation.data,
                    'meets_criteria': form.meets_criteria.data
                },
                'attitude': {
                    'voice_tone': form.voice_tone.data,
                    'empathy': form.empathy.data,
                    'words_repeat': form.words_repeat.data,
                    'treat_you': form.treat_you.data,
                    'secure_presentation': form.secure_presentation.data
                },
                'negotiation_one': {
                    'start_negotiation': form.start_negotiation.data,
                    'active_listening': form.active_listening.data,
                    'preparation': form.preparation.data
                },
                'negotiation_two': {
                    'negotiation_two': form.negotiation_two.data
                },
                'registration_one': {
                    'collector_registration': form.collector_registration.data,
                    'managementes_result': form.managementes_result.data,
                    'new_debtor_data': form.new_debtor_data.data,
                    'generate_promise': form.generate_promise.data,
                    'load_promise_managment': form.load_promise_managment.data
                },
                'registration_two': {
                    'add_contact': form.add_contact.data,
                    'writing_field': form.writing_field.data,
                    'abbreviations': form.abbreviations.data
                },
                'closing': {
                    'successful': form.successful.data,
                    'not_successful': form.not_successful.data,
                    'remember_date': form.remember_date.data,
                    'provide_data': form.provide_data.data
                }
            }

    def action(self) -> dict:
        salute = self.salute(self.data['salute'])
        attitude = self.attitude(self.data['attitude'])
        negotiation_one = self.negotiation_one(self.data['negotiation_one'])
        negotiation_two = self.negotiation_two(self.data['negotiation_two'])
        registration_one = self.registration_one(self.data['registration_one'])
        registration_two = self.registration_two(self.data['registration_two'])
        closing = self.closing(self.data['closing'])
        
        # Sumar el total
        result = salute + attitude + negotiation_one + negotiation_two + registration_one + registration_two + closing

        # Comprobar si la negociacion 2 es 0
        if negotiation_two == 0:
            result = 0


        # Crear objeto a retornar
        data_result = {
            "salute": salute,
            "attitude": attitude,
            "negotiation_one": negotiation_one,
            "negotiation_two": negotiation_two,
            "registration_one": registration_one,
            "registration_two": registration_two,
            "closing": closing,
            "result": float('{0: .2f}'.format(result))
        }
        
        return data_result

    def salute(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Saludo
        """
        identity_holder = 0.2 if data["identity_holder"] else 0
        presentation = 0.2 if data["presentation"] else 0
        presentation_company = 0.2 if data["presentation_company"] else 0
        debt_presentation = 0.2 if data["debt_presentation"] else 0
        meets_criteria = 0.2 if data["meets_criteria"] else 0

        result = identity_holder + presentation + presentation_company + debt_presentation + meets_criteria

        return float('{0: 2f}'.format(result))

    def attitude(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Actitud
        """
        voice_tone = 0.6 if data["voice_tone"] else 0
        empathy = 0.6 if data["empathy"] else 0
        words_repeat = 0.6 if data["words_repeat"] else 0
        treat_you = 0.6 if data["treat_you"] else 0
        secure_presentation = 0.6 if data["secure_presentation"] else 0

        result = voice_tone + empathy + words_repeat + treat_you + secure_presentation

        return float('{0: .2f}'.format(result))

    def negotiation_one(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Negociacion 1
        """
        start_negotiation = 0.3 if data["start_negotiation"] else 0
        active_listening = 0.4 if data["active_listening"] else 0
        preparation = 0.3 if data["preparation"] else 0

        negotiation_one = start_negotiation + active_listening + preparation

        return float('{0: .2f}'.format(negotiation_one))

    def negotiation_two(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Negociacion 2
        """
        negotiation_two = 1 if data["negotiation_two"] else 0

        return float('{0: .2f}'.format(negotiation_two))

    def registration_one(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Registro 1
        """
        collector_registration = 0.5 if data["collector_registration"] else 0
        managementes_result = 0.5 if data["managementes_result"] else 0
        new_debtor_data = 0.5 if data["new_debtor_data"] else 0
        generate_promise = 0.5 if data["generate_promise"] else 0

        registration_one = collector_registration + managementes_result + new_debtor_data + generate_promise

        return float('{0: .2f}'.format(registration_one))

    def registration_two(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Registro 2
        """
        add_contact = 0.3 if data["add_contact"] else 0
        writing_field = 0.4 if data["writing_field"] else 0
        abbreviations = 0.3 if data["abbreviations"] else 0

        registration_two = add_contact + writing_field + abbreviations

        return float('{0: .2f}'.format(registration_two))

    def closing(self, data: dict) -> float:
        """
            Funcion donde se calcula los resultados del Item Cerrar
        """
        successful = 0.4 if data["successful"] or data["not_successful"] else 0
        remember_date = 0.3 if data["remember_date"] else 0
        provide_data = 0.3 if data["provide_data"] else 0

        closing = successful + remember_date + provide_data

        return float('{0: .2f}'.format(closing))
