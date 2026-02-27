import importlib

def generate_chameleon_pdf(output_filename, tailored_data, template_choice):
    
    #The Switchboard: Dynamically imports the user's chosen template.
    #right now only for template1, but this allows for easy expansion to more designs in the future.
    
    try:
        # This line dynamically imports 'templates/template1.py' based on user input
        template_module = importlib.import_module(f"templates.{template_choice}")
        
        # Every template file must have a function named 'render'
        template_module.render(output_filename, tailored_data)
        
        print(f"Resume Chameleon successfully applied: {template_choice}")
        
    except ImportError:
        print(f"Error: Template '{template_choice}' not found.")
    except Exception as e:
        print(f"Error generating PDF: {e}")