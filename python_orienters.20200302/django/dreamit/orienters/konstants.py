records_per_page = 5

default_user_name = 'Anon'

gender_choices=[('male','Male'), ('female','Female')]

identifier_illuminator_toc = [
    'Asserting: Focusing and Achieving',
    'Producing: Maintaining and Delivering',
    'Thinking: Expressing and Communicating',
    'Protecting: Reacting and Sharing',
    'Creating: Energising and Illuminating',
    'Analysing: Clarifying and Resolving',
    'Relating: Evaluating and Reflecting',
    'Transforming: Deepening and Realising',
    'Developing: Growing and Discovering',
    'Organising: Establishing and Structuring',
    'Progressing: Originating and Fulfilling',
    'Imagining: Perceiving and Visualising']

self_patterns = [
    'Self-Acceptance',
    'Self-Assertion',
    'Self-Worth',
    'Self-Knowledge',
    'Self-Affirmation',
    'Self-Respect',
    'Self-Analysis',
    'Self-Determination',
    'Self-Empowerment',
    'Self-Exploration',
    'Self-Control',
    'Self-Realisation',
    'Self-Acceptance']

# The first & second duplicates are intentional
base_methods = [
    'Assert',
    'Assert',
    'Produce',
    'Think',
    'Protect',
    'Create',
    'Analyse',
    'Relate',
    'Transform',
    'Develop',
    'Organise',
    'Progress',
    'Imagine']

self_methods = base_methods

voice_patterns = [
    'Accepter',
    'Achiever',
    'Fixer',
    'Talker',
    'Protector',
    'Creator',
    'Critic',
    'Pleaser',
    'Desirer',
    'Seeker',
    'Controller',
    'Rebel',
    'Accepter']

# The first & second duplicates are intentional
voice_methods = base_methods

place_patterns = [
    'Imagination',
    'Action',
    'Stability',
    'Thought',
    'Security',
    'Cadence',
    'Analysis',
    'Balance',
    'Purpose',
    'Growth',
    'Structure',
    'Change',
    'Imagination']

place_methods = base_methods

event_patterns = [
    'Transcending',
    'Uniting',
    'Separating',
    'Supporting',
    'Challenging',
    'Creating',
    'Helping',
    'Deciding',
    'Transforming',
    'Generating',
    'Consolidating',
    'Liberating',
    'Transcending']

event_methods = base_methods

object_patterns = [
    'Inspirational',
    'Independent',
    'Financial',
    'Versatile',
    'Protective',
    'Creative',
    'Precision',
    'Collaborative',
    'Power',
    'Travel',
    'Authority',
    'Unique',
    'Inspirational']

# The first & second duplicates are intentional
object_methods = base_methods

person_patterns  = [
    'Dreamer',
    'Pioneer',
    'Farmer',
    'Journalist',
    'Nurturer',
    'Performer',
    'Doctor',
    'Artist',
    'Magician',
    'Explorer',
    'Builder',
    'Inventor',
    'Dreamer']

# The first & second duplicates are intentional
person_methods  = base_methods

## start : illuminator
input_type_choices=[(1,'Text'),(2,'Sound'),(3,'Image'),(4,'Video')]

input_method_choices=[(1,'Embed'),(2,'Link'),(3,'Upload')]
## end : illuminator

## start : connector
ing_cadence=[
    'Asserting',
    'Producing',
    'Thinking',
    'Responding',
    'Creating',
    'Analysing',
    'Relating',
    'Transforming',
    'Developing',
    'Organising',
    'Progressing',
    'Imagining']

## See line 224 in www/wp-content/plugins/dreamit-connectors.php
connector_patterns = person_patterns

# The first & second duplicates are intentional
connector_methods = base_methods
## end : connector

def get_en_data(patterns):
    en_data = {}

    en_data[patterns[1]] = {'x':216, 'y':40, 'color':0}
    # en_data[self_patterns[1]]['x'] = 216
    # en_data[self_patterns[1]]['y'] = 40
    # en_data[self_patterns[1]]['color'] = 0
    en_data[patterns[2]] = {'x':105, 'y':105, 'color':0}
    # en_data[self_patterns[2]]['x'] = 105
    # en_data[self_patterns[2]]['y'] = 105
    # en_data[self_patterns[2]]['color'] = 0
    en_data[patterns[3]] = {'x':40, 'y':220, 'color':0}
    # en_data[self_patterns[3]]['x'] = 40
    # en_data[self_patterns[3]]['y'] = 220
    # en_data[self_patterns[3]]['color'] = 0
    en_data[patterns[4]] = {'x':50, 'y':340, 'color':0}
    # en_data[self_patterns[4]]['x'] = 50
    # en_data[self_patterns[4]]['y'] = 340
    # en_data[self_patterns[4]]['color'] = 0
    en_data[patterns[5]] = {'x':110, 'y':460, 'color':0}
    # en_data[self_patterns[5]]['x'] = 110
    # en_data[self_patterns[5]]['y'] = 460
    # en_data[self_patterns[5]]['color']  = 0
    en_data[patterns[6]] = {'x':220, 'y':525, 'color':0}
    # en_data[self_patterns[6]]['x'] = 220
    # en_data[self_patterns[6]]['y'] = 525
    # en_data[self_patterns[6]]['color'] = 0
    en_data[patterns[7]] = {'x':340, 'y':525, 'color':0}
    # en_data[self_patterns[7]]['x'] = 340
    # en_data[self_patterns[7]]['y'] = 525
    # en_data[self_patterns[7]]['color'] = 0
    en_data[patterns[8]] = {'x':456, 'y':460, 'color':0}
    # en_data[self_patterns[8]]['x'] = 456
    # en_data[self_patterns[8]]['y'] = 460
    # en_data[self_patterns[8]]['color'] = 0
    en_data[patterns[9]] = {'x':525, 'y':340, 'color':0}
    # en_data[self_patterns[9]]['x'] = 525
    # en_data[self_patterns[9]]['y'] = 340
    # en_data[self_patterns[9]]['color'] = 0
    en_data[patterns[10]] = {'x':520, 'y':220, 'color':0}
    # en_data[self_patterns[10]]['x'] = 520
    # en_data[self_patterns[10]]['y'] = 220
    # en_data[self_patterns[10]]['color'] = 0
    en_data[patterns[11]] = {'x':455, 'y':110, 'color':0}
    # en_data[self_patterns[11]]['x'] = 455
    # en_data[self_patterns[11]]['y'] = 110
    # en_data[self_patterns[11]]['color'] = 0
    en_data[patterns[12]] = {'x':345, 'y':40, 'color':0}
    # en_data[self_patterns[12]]['x'] = 345
    # en_data[self_patterns[12]]['y'] = 40
    # en_data[self_patterns[12]]['color'] = 0

    return en_data
