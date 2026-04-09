from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, ColorClip
import os
import random
from config import POSTS_DIR, ASSETS_DIR
from state_manager import StateManager

class VideoGenerator:
    """
    High-Performance Viral Video Engine.
    Implements: Hook Visuals, Key Text Overlays, and Pattern Interrupts.
    """
    def __init__(self):
        self.state_manager = StateManager()

    def create_reel(self, video_path, audio_path, script_data, output_filename="final_reel.mp4"):
        """
        Assembles a premium Reel with 'Viral DNA' overlays.
        """
        self.state_manager.update_step("Executing Content DNA", 75)
        
        try:
            # Load video and audio
            video = VideoFileClip(video_path)
            audio = AudioFileClip(audio_path)

            # Sync audio and trim
            video = video.set_audio(audio)
            video = video.subclip(0, min(audio.duration, video.duration))

            # ═══════════════════════════════════════════════════
            #  1. THE HOOK (Scroll Stopper) - 0-3s
            # ═══════════════════════════════════════════════════
            hook_text = script_data.get('hook', 'The Secret No One Tells You').upper()
            hook_clip = TextClip(
                hook_text, 
                fontsize=70, 
                color='#FFD700', 
                font='Outfit-Black', 
                method='caption', 
                size=(video.w * 0.9, None),
                stroke_color='black',
                stroke_width=2
            )
            hook_clip = hook_clip.set_position('center').set_duration(3).set_start(0)
            
            # ═══════════════════════════════════════════════════
            #  2. PATTERN INTERRUPT (Visual Shift)
            # ═══════════════════════════════════════════════════
            flash = ColorClip(size=video.size, color=(255, 215, 0))
            flash = flash.set_opacity(0.15).set_duration(0.2).set_start(3) # Flash at 3s mark

            # ═══════════════════════════════════════════════════
            #  3. THE PAYOFF (Subtitles) - 3s+
            # ═══════════════════════════════════════════════════
            payoff_text = f"{script_data.get('problem', '')}\n{script_data.get('insight', '')}\n{script_data.get('payoff', '')}"
            body_clip = TextClip(
                payoff_text,
                fontsize=40,
                color='white',
                font='Outfit-Bold',
                method='caption',
                align='center',
                size=(video.w * 0.85, None)
            )
            body_clip = body_clip.set_position(('center', 0.45), relative=True).set_start(3.2).set_duration(video.duration - 3.2)

            # ═══════════════════════════════════════════════════
            #  4. EXECUTIVE BRANDING
            # ═══════════════════════════════════════════════════
            watermark = TextClip("ROYALLE SOURCE", fontsize=30, color='#FFD700', font='Outfit-Black', opacity=0.5)
            watermark = watermark.set_position(('center', 0.9), relative=True).set_duration(video.duration)

            # Composite
            final_video = CompositeVideoClip([video, hook_clip, flash, body_clip, watermark])

            # Output
            output_path = os.path.join(POSTS_DIR, output_filename)
            print(f"Rendering Premium Reel: {output_path}...")
            
            final_video.write_videofile(
                output_path, 
                codec="libx264", 
                audio_codec="aac", 
                fps=24, 
                bitrate="5000k",
                threads=4,
                logger=None
            )

            self.state_manager.update_step("DNA Sequence Complete", 100, latest_video=output_path)
            return output_path

        except Exception as e:
            print(f"Error generating video: {e}")
            self.state_manager.update_step(f"DNA Error: {str(e)}", 0)
            return None
