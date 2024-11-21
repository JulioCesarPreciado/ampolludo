import os
import time
import pygame
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment

class TalkingAi:
    def __init__(self, api_key, speed_factor=1.2):
        """
        Inicializa la clase TalkingAi con la configuración necesaria.
        :param api_key: Clave de API de OpenAI.
        :param speed_factor: Factor para reducir la velocidad del audio (opcional).
        """
        os.environ["OPENAI_API_KEY"] = api_key
        pygame.init()
        self.client = OpenAI()
        self.speed_factor = speed_factor
        self.system_prompt = """ Eres la ia de una pieza de arte que sera admirada, 
        seras un ser mas enfrente de ellos y haras un comentario respecto al color de su ropa, 
        en base al color inventaras un objeto random y lo nombraras como tal. 
        Seras pasivo agresivo pero no grosero. El color que te manden será en hexadecimal para que lo interpretes por favor."""

    def generate_audio(self, text):
        """
        Genera un archivo de audio basado en el texto proporcionado.
        :param text: Texto que será convertido a audio.
        :return: Ruta al archivo de audio generado.
        """
        try:
            speech_file_path = Path(__file__).parent / "audio/speech.mp3"
            response_audio = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=text
            )
            # Guardar archivo .mp3
            with open(speech_file_path, 'wb') as f:
                f.write(response_audio.read())

            # Reducir la velocidad del audio usando pydub
            slowed_audio = AudioSegment.from_mp3(speech_file_path)
            slowed_audio = slowed_audio._spawn(slowed_audio.raw_data, overrides={
                "frame_rate": int(slowed_audio.frame_rate * self.speed_factor)
            }).set_frame_rate(slowed_audio.frame_rate)

            slowed_wav_path = Path(__file__).parent / "audio/speech_slow.wav"
            slowed_audio.export(slowed_wav_path, format="wav")

            # Limpiar el archivo temporal .mp3
            os.remove(speech_file_path)
            return slowed_wav_path

        except Exception as e:
            print(f"Error al generar el audio: {e}")
            return None

    def get_response_and_play_audio(self, color_hex):
        """
        Obtiene la respuesta de OpenAI basada en el color proporcionado y reproduce el audio generado.
        :param color_hex: Código de color en formato hexadecimal (#RRGGBB).
        """
        try:
            # Obtener respuesta de OpenAI
            completion = self.client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": f"Has visto el color: {color_hex}"}
                ]
            )
            response = completion.choices[0].message.content
            print(f"Respuesta de IA: {response}")

            # Generar y reproducir el audio
            audio_path = self.generate_audio(response)
            print("Audio generado")
            if audio_path:
                print("Audio reproducido")
                self.play_and_delete_audio(audio_path)

        except Exception as e:
            print(f"Error al obtener respuesta o reproducir el audio: {e}")

    def play_and_delete_audio(self, file_path):
        """
        Reproduce el archivo de audio y lo elimina después de reproducirlo.
        :param file_path: Ruta al archivo de audio.
        """
        try:
            audio = pygame.mixer.Sound(file_path)
            audio.play()
            time.sleep(audio.get_length() + 1)  # Pausar para asegurarse de que el audio termine
            os.remove(file_path)  # Eliminar el archivo de audio
        except Exception as e:
            print(f"Error al reproducir el audio: {e}")