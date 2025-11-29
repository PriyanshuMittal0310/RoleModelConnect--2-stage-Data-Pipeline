# Phase 2: Data Curation Pipeline
# Interactive JSON Entry Creator for RoleModelConnect
# This script loads raw .txt files and guides you through creating structured JSON entries

import json
import os
from pathlib import Path

# Configuration
RAW_DATA_FOLDER = "Raw_Data"
OUTPUT_FOLDER = "Generated_JSON_Entries"

# Create output folder if it doesn't exist
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Valid mental health themes
MENTAL_HEALTH_THEMES = [
    "anxiety",
    "depression",
    "stress_management",
    "burnout",
    "grief",
    "addiction_recovery",
    "imposter_syndrome",
    "self_esteem",
    "relationship_challenges",
    "public_pressure"
]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def sanitize_role_model_name(name: str) -> str:
    """Make role model name safe for filenames."""
    return name.replace(" ", "").replace("'", "")


def infer_role_model_name_from_raw(raw_content: str):
    """
    Try to infer the role model name from the header in the raw .txt file.
    Looks for a line starting with 'Role Model:'.
    """
    for line in raw_content.splitlines():
        if line.lower().startswith("role model:"):
            return line.split(":", 1)[1].strip()
    return None


def get_or_confirm_role_model_name(raw_content: str):
    """
    Prefer the name inferred from the raw file header; allow the user to override.
    Falls back to manual input if nothing is inferred.
    """
    inferred = infer_role_model_name_from_raw(raw_content)
    if inferred:
        print(f"\nDetected role model name from raw file header: '{inferred}'")
        user_input = input("Press Enter to confirm, or type a different name to override: ").strip()
        if user_input:
            return user_input
        return inferred
    else:
        # Use existing manual function as fallback
        return get_role_model_name()


def get_next_story_number(role_model_name: str, roll_number: str) -> int:
    """
    Compute the next StoryNumber for this role model + roll number
    by scanning existing JSON files in OUTPUT_FOLDER.

    File pattern: RoleModelName_StoryNumber_YourRollNumber.json
    """
    clean_name = sanitize_role_model_name(role_model_name)
    existing_numbers = []

    for fname in os.listdir(OUTPUT_FOLDER):
        if not fname.endswith(".json"):
            continue
        parts = fname.split("_")
        if len(parts) < 3:
            continue

        file_clean_name = parts[0]
        story_part = parts[1]
        roll_part = parts[2].split(".")[0]

        if file_clean_name != clean_name:
            continue
        if roll_part != roll_number:
            continue

        try:
            existing_numbers.append(int(story_part))
        except ValueError:
            continue

    if not existing_numbers:
        return 1
    return max(existing_numbers) + 1

def display_available_files():
    """Display all raw .txt files available for curation"""
    raw_files = list(Path(RAW_DATA_FOLDER).glob("*.txt"))
    
    if not raw_files:
        print(f"\n⚠ No files found in {RAW_DATA_FOLDER}/ folder")
        print("Please run Phase 1 (data collection) first.")
        return []
    
    print(f"\n{'='*80}")
    print("AVAILABLE RAW DATA FILES")
    print(f"{'='*80}")
    
    for i, filepath in enumerate(sorted(raw_files), 1):
        file_size = filepath.stat().st_size / 1024  # Size in KB
        print(f"{i}. {filepath.name} ({file_size:.1f} KB)")
    
    return sorted(raw_files)

def select_raw_file(available_files):
    """Let user select a raw .txt file to curate"""
    while True:
        try:
            choice = int(input("\nEnter file number to curate (or 0 to exit): "))
            if choice == 0:
                return None
            if 1 <= choice <= len(available_files):
                return available_files[choice - 1]
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def display_raw_content(filepath, preview_length=1500):
    """Display preview of raw .txt file content"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print(f"\n{'='*80}")
    print(f"CONTENT PREVIEW: {filepath.name}")
    print(f"{'='*80}\n")
    
    # Display first preview_length characters
    preview = content[:preview_length]
    print(preview)
    
    if len(content) > preview_length:
        print(f"\n... ({len(content) - preview_length} more characters)")
    
    print(f"\n{'='*80}")
    return content

def get_role_model_name():
    """Get role model name from user"""
    while True:
        name = input("\nEnter Role Model Name (full name, e.g., 'Selena Gomez'): ").strip()
        if name and len(name) >= 2:
            return name
        print("Please enter a valid name.")

def get_context(name):
    """Get 1-sentence context about the role model"""
    print(f"\nExample: 'American singer, actress, and mental health advocate'")
    context = input(f"Enter {name}'s context (1 sentence): ").strip()
    
    while not context or len(context) < 10:
        context = input("Please enter a meaningful context (minimum 10 characters): ").strip()
    
    return context

def get_situation_faced():
    """Get the specific situation/challenge faced"""
    print("\nExample: 'Struggles with anxiety and depression while maintaining a public career'")
    situation = input("What specific situation did they face?: ").strip()
    
    while not situation or len(situation) < 10:
        situation = input("Please enter a specific situation (minimum 10 characters): ").strip()
    
    return situation

def get_challenge_narrative():
    """Get 2-3 sentence narrative of the challenge"""
    print("\nEnter a 2-3 sentence factual summary (derived from raw text):")
    narrative = input("Challenge Narrative: ").strip()
    
    while not narrative or len(narrative) < 20:
        narrative = input("Please enter a detailed narrative (minimum 20 characters): ").strip()
    
    return narrative

def select_mental_health_themes():
    """Let user select 2-4 mental health themes"""
    print(f"\n{'='*80}")
    print("SELECT MENTAL HEALTH THEMES (Choose 2-4)")
    print(f"{'='*80}\n")
    
    for i, theme in enumerate(MENTAL_HEALTH_THEMES, 1):
        print(f"{i}. {theme}")
    
    selected = []
    while len(selected) < 2 or len(selected) > 4:
        try:
            choices = input("\nEnter theme numbers (comma-separated, e.g., '1,3,5'): ").split(',')
            choices = [int(c.strip()) - 1 for c in choices]
            
            if all(0 <= c < len(MENTAL_HEALTH_THEMES) for c in choices):
                if 2 <= len(choices) <= 4:
                    selected = [MENTAL_HEALTH_THEMES[c] for c in choices]
                else:
                    print("Please select between 2 and 4 themes.")
            else:
                print("Invalid choice. Please enter valid theme numbers.")
        except ValueError:
            print("Please enter valid numbers separated by commas.")
    
    return selected

def get_coping_strategies():
    """Get list of coping strategies used"""
    print("\nExamples: therapy, meditation, taking breaks, medication, exercise, journaling")
    print("Enter coping strategies (comma-separated):")
    strategies_input = input("Coping Strategies: ").strip()
    
    while not strategies_input or len(strategies_input) < 5:
        strategies_input = input("Please enter at least one strategy: ").strip()
    
    # Clean and split strategies
    strategies = [s.strip() for s in strategies_input.split(',') if s.strip()]
    return strategies

def get_key_action():
    """Get the key action taken"""
    print("\nExamples: 'Entered rehab facility', 'Started therapy', 'Took a break from work'")
    action = input("Key Action Taken: ").strip()
    
    while not action or len(action) < 5:
        action = input("Please enter a specific key action: ").strip()
    
    return action

def get_quote_from_text(raw_content):
    """Guide user to find and extract a quote from raw text"""
    print(f"\n{'='*80}")
    print("EXTRACT A DIRECT QUOTE FROM RAW TEXT")
    print(f"{'='*80}")
    print("\nReview the content preview above and find a powerful, relevant quote.")
    print("Enter the exact quote (must be from the raw text):\n")
    
    quote = input("Direct Quote: ").strip()
    
    while not quote or len(quote) < 10:
        quote = input("Please enter a valid quote (minimum 10 characters): ").strip()
    
    # Verify quote exists in raw content
    if quote.lower() not in raw_content.lower():
        confirm = input("\n⚠ Quote not found in raw text. Continue anyway? (y/n): ").lower()
        if confirm != 'y':
            return get_quote_from_text(raw_content)
    
    return quote

def get_psychological_lesson():
    """Get 2-3 sentence psychological lesson"""
    print("\nWhat psychological or life lesson can we draw from this story?")
    print("(2-3 sentences):")
    lesson = input("Psychological Lesson: ").strip()
    
    while not lesson or len(lesson) < 20:
        lesson = input("Please enter a meaningful lesson (minimum 20 characters): ").strip()
    
    return lesson

def get_outcome_resolution():
    """Get the outcome/resolution"""
    print("\nWhat was the behavioral or ethical resolution?")
    outcome = input("Outcome/Resolution: ").strip()
    
    while not outcome or len(outcome) < 10:
        outcome = input("Please enter the outcome (minimum 10 characters): ").strip()
    
    return outcome

def get_source_reference(filepath):
    """Display source file reference"""
    source_name = filepath.name
    print(f"\n✓ Source Reference: {source_name}")
    return source_name

def create_json_entry(raw_filepath, roll_number):
    """Interactive JSON entry creation"""
    # Display raw content first
    raw_content = display_raw_content(raw_filepath)

    # Get / confirm role model name
    role_model_name = get_or_confirm_role_model_name(raw_content)

    # Compute the next story number for this role model + roll number
    story_number = get_next_story_number(role_model_name, roll_number)

    print(f"\n\n{'#'*80}")
    print(f"# CREATING JSON ENTRY #{story_number} for {role_model_name}")
    print(f"{'#'*80}")

    # Collect all information
    context = get_context(role_model_name)
    situation = get_situation_faced()
    narrative = get_challenge_narrative()
    themes = select_mental_health_themes()
    strategies = get_coping_strategies()
    action = get_key_action()
    quote = get_quote_from_text(raw_content)
    lesson = get_psychological_lesson()
    outcome = get_outcome_resolution()
    source = get_source_reference(raw_filepath)

    # Create JSON structure
    json_entry = {
        "Role_Model_Name": role_model_name,
        "Role_Model_Context": context,
        "Situation_Faced": situation,
        "Challenge_Narrative": narrative,
        "Mental_Health_Themes": themes,
        "Coping_Strategies_Used": strategies,
        "Key_Action_Taken": action,
        "Key_Quote_or_Insight": quote,
        "Summary_Psychological": lesson,
        "Outcome_Resolution": outcome,
        "Source_Reference": source
    }

    # Create clean role model name for filename
    clean_name = sanitize_role_model_name(role_model_name)

    # Save JSON file
    output_filename = f"{clean_name}_{story_number}_{roll_number}.json"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(json_entry, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*80}")
    print(f"✓ JSON ENTRY CREATED SUCCESSFULLY")
    print(f"{'='*80}")
    print(f"Saved to: {output_path}")
    print(f"File: {output_filename}")

    return output_path, json_entry

def display_json_summary(json_entry):
    """Display a summary of the created JSON entry"""
    print(f"\n{'='*80}")
    print("JSON ENTRY SUMMARY")
    print(f"{'='*80}\n")
    
    print(f"Role Model: {json_entry['Role_Model_Name']}")
    print(f"Context: {json_entry['Role_Model_Context']}")
    print(f"Situation: {json_entry['Situation_Faced']}")
    print(f"\nThemes: {', '.join(json_entry['Mental_Health_Themes'])}")
    print(f"Strategies: {', '.join(json_entry['Coping_Strategies_Used'])}")
    print(f"\nKey Action: {json_entry['Key_Action_Taken']}")
    print(f"\nQuote: \"{json_entry['Key_Quote_or_Insight']}\"")
    print(f"\nSource: {json_entry['Source_Reference']}")
    print(f"{'='*80}\n")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main curation workflow"""
    print(f"\n{'='*80}")
    print("ROLEMODELSCONNECT - PHASE 2: DATA CURATION PIPELINE")
    print(f"{'='*80}")

    # Get user's roll number
    roll_number = input("\nEnter your Roll Number: ").strip()
    while not roll_number:
        roll_number = input("Please enter a valid roll number: ").strip()

    total_entries_created = 0

    # Main workflow loop
    while True:
        # Display available files
        available_files = display_available_files()

        if not available_files:
            break

        # Select file to curate
        selected_file = select_raw_file(available_files)
        if not selected_file:
            break

        # Ask how many entries from this file
        while True:
            try:
                num_entries = int(input("\nHow many JSON entries from this file? (1-3): "))
                if 1 <= num_entries <= 3:
                    break
                else:
                    print("Please enter 1, 2, or 3.")
            except ValueError:
                print("Please enter a valid number.")

        # Create JSON entries
        for _ in range(num_entries):
            output_path, json_data = create_json_entry(selected_file, roll_number)
            display_json_summary(json_data)
            total_entries_created += 1

            input("\nPress Enter to continue...")

        # Ask if user wants to curate another file
        continue_choice = input("\nCreate entries from another file? (y/n): ").lower()
        if continue_choice != 'y':
            break

    # Final summary
    print(f"\n{'='*80}")
    print("CURATION COMPLETE")
    print(f"{'='*80}")
    print(f"Total JSON entries created: {total_entries_created}")
    print(f"Saved in: {OUTPUT_FOLDER}/")
    print("\nVerify each JSON file:")
    print("✓ All quotes are from raw text files")
    print("✓ Source_Reference matches actual filenames")
    print("✓ Mental health themes are from the provided list")
    print("✓ All required fields are filled")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    main()