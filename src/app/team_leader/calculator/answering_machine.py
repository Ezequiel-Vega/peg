from .interface_calculator import ICalculator
from app.team_leader.forms import AnsweringMachine

class AnsweringMachineCalculator(ICalculator):
    """
        Calculador de resultado Contestador
    """
    def __init__(self, form: AnsweringMachine) -> None:
        self.data = {
            'salute': {
                'info_holder': form.info_holder.data,
                'presentation': form.presentation.data,
                'presentation_company': form.presentation_company.data,
                'reason_call': form.reason_call.data
            },
            'attitude': {
                'voice_tone': form.voice_tone.data,
                'words_repeat': form.words_repeat.data,
                'secure_presentation': form.secure_presentation.data
            },
            'message': {
                'message': form.message.data
            },
            'registration_one': {
                'collector_registration': form.collector_registration.data,
                'managementes_result': form.managementes_result.data
            },
            'registration_two': {
                'open_call_yes': form.open_call_yes.data,
                'open_call_no': form.open_call_no.data,
                'add_contact': form.add_contact.data,
                'writing_field': form.writing_field.data,
                'abbreviations': form.abbreviations.data
            }
        }

    def action(self) -> dict:
        # Calcular los resultados individualmente
        salute = self.salute(self.data["salute"])
        attitude = self.attitude(self.data["attitude"])
        message = self.message(self.data["message"])
        registration_one = self.registration_one(self.data["registration_one"])
        registration_two = self.registration_two(self.data["registration_two"])

        # Sumar el total
        result = salute + attitude + message + registration_one + registration_two

        # Comprobar si la negociacion 2 es 0
        if message == 0:
            result = 0

        # Crear objeto a retornar
        data_result = {
            "salute": salute,
            "attitude": attitude,
            "message": message,
            "negotiation_one": None,
            "negotiation_two": None,
            "registration_one": registration_one,
            "registration_two": registration_two,
            "result": float('{0: .2f}'.format(result))
        }

        # Retornar resultado
        return data_result
        
    def salute(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Saludo
        """
        
        info_holder = 0.25 if data['info_holder'] else 0
            
        presentation = 0.25 if data['presentation'] else 0
            
        presentation_company = 0.25 if data['presentation_company'] else 0           
        
        reason_call = 0.25 if data['reason_call'] else 0 

        salute = info_holder + presentation + presentation_company + reason_call
        
        return float('{0: .2f}'.format(salute))

    def attitude(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Actitud
        """

        voice_tone = 1 if data['voice_tone'] else 0 
        
        words_repeat = 1 if data['words_repeat'] else 0
        
        secure_presentation = 1 if data['secure_presentation'] else 0 

        attitude = voice_tone + words_repeat + secure_presentation

        return float('{0: .2f}'.format(attitude))

    def message(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Mensaje
        """

        message = 3 if data['message'] else 0 
        
        return float('{0: .2f}'.format(message))

    def registration_one(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Registro 1
        """

        collector_registration = 1 if data['collector_registration'] else 0
        
        managementes_result = 1 if data['managementes_result'] else 0 
        
        registration_one = collector_registration + managementes_result

        return float('{0: .2f}'.format(registration_one))

    def registration_two(self, data: dict) -> float:
        """
            Se calcula los resultados del Item Registro 2
        """

        open_call = 0
        if data['open_call_no'] == True and data['open_call_yes']:
            open_call = 0
             

        add_contact = 0.3 if data['add_contact'] else 0 
        
        writing_field = 0.4 if data['writing_field'] else 0 
        
        abbreviations = 0.3 if data['abbreviations'] else 0
            
        
        if data['open_call_yes']:
            registration_two = 0
        else:
            registration_two = add_contact + writing_field + abbreviations + open_call
        
        return float('{0: .2f}'.format(registration_two))
