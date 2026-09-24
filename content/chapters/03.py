PAGES.extend([{'slug': 'intelligence',
  'label': 'Personal AI & privacy',
  'title': 'Personal AI.<br>On your terms.',
  'intro': 'Personal AI could help you understand information, reflect on experience and make choices. '
           'Mutual Futures connects that capability with GAJRA’s question of alignment: does the system '
           'help you act on what matters to you, under permissions you can understand?',
  'image': 'australian-design',
  'accent': 'violet',
  'tool': 'permissions',
  'sections': [{'title': 'Begin with a person’s purpose',
                'text': 'Aura of Intelligence is a developing design for personal AI. The aim is to '
                        'help a person organise knowledge, reflect on experiences and choose what to '
                        'share. A useful starting task might be preparing for a new role, finding a '
                        'source or comparing a decision with personal priorities.\n'
                        '\n'
                        'The project’s proposed cognitive architecture remains research and '
                        'development. Its technical design is documented in the Aura project; this site '
                        'focuses on the person’s choices and the work a system would need to perform.',
                'cards': [{'title': 'Human self-alignment and AI alignment',
                           'text': 'See how personal reflection connects with evaluation and correction '
                                   'of AI systems.',
                           'href': 'gajra.html'}],
                'refs': ['P02', 'D13']},
               {'title': 'Use computing at the scale the task needs',
                'text': 'Personal devices, shared local facilities, regional infrastructure and cloud '
                        'services can each have a role. Choose around the task, operating cost, energy, '
                        'access and the information involved. Shared computing could support enterprise '
                        'design and learning without making every person dependent on one provider.',
                'refs': ['D03', 'D13']},
               {'title': 'Connecting personal AI with legal information',
                'text': 'A future Aura system could help people find and understand legal sources. The '
                        'Australian Law 2012 project explains the original approach, and a separate '
                        'Australian Legal Engine repository describes tools for finding and tracing '
                        'legal provisions. Integration with the Aura app remains unfinished.',
                'refs': ['P08', 'P09']},
               {'title': 'Choose how information may be used',
                'text': 'Using information to answer a question is different from using it to train an '
                        'AI model. Keeping it on an approved local system is different from sharing it '
                        'with an external service. The case study below explains why those choices '
                        'matter. The builder records preferences; it does not enforce them.',
                'cards': [{'title': 'Personal',
                           'text': "The person's own values, memories, choices and preferred models.",
                           'href': None},
                          {'title': 'Professional',
                           'text': 'The qualifications and relevant information a role genuinely '
                                   'requires.',
                           'href': None},
                          {'title': 'Collective',
                           'text': 'Material whose custodians or communities determine the relevant '
                                   'authority and permissions.',
                           'href': None}],
                'refs': ['P02', 'P05', 'S07']},
               {'title': 'Make responsibilities clear',
                'text': 'Before a person, AI system or robot carries out a task, the people involved '
                        'should understand its purpose, who authorised it, what skills and information '
                        'it needs, and who checks the result. There also needs to be a way to stop, '
                        'correct mistakes and recover.'}]},
 {'slug': 'law',
  'label': 'Legal reflection',
  'title': 'Understand the rules.<br>Help shape better ones.',
  'intro': 'Laws affect our work, homes and shared future. This part of the proposal asks how people '
           'could understand those rules, see their effects and explore changes through lawful public '
           'processes.',
  'image': 'law',
  'accent': 'gold',
  'sections': [{'title': 'Where this approach began',
                'text': 'In 2012 and 2013, Luke Nathan Hayes read through Australian legal material to '
                        'understand its relevance to his own life. He called his method Gather, Chomp, '
                        'Sort, Plan: collect sources, work through them, organise what matters and '
                        'decide what to do next. That work informs this proposal for making legal '
                        'information easier to explore.',
                'refs': ['P08']},
               {'title': 'Keep these three questions clear',
                'text': '',
                'cards': [{'title': 'Current obligations and rights',
                           'text': 'Applicable sources, jurisdiction, commencement, version and '
                                   'unresolved interpretation.',
                           'href': None},
                          {'title': 'Voluntary commitments',
                           'text': 'Additional practices an individual or organisation has chosen, '
                                   'clearly distinguished from legal requirements.',
                           'href': None},
                          {'title': 'Proposed changes',
                           'text': 'Alternative wording or arrangements, assumptions, consultation and '
                                   'modelled consequences.',
                           'href': None}]},
               {'title': 'Look at how the rules work together',
                'text': 'Understanding a legal question may involve national, state and local rules, '
                        'court decisions, contracts, standards and international agreements. Each '
                        'source needs its date, version and legal status recorded. The wording of a '
                        'rule and an interpretation of how it applies should remain clearly identified.',
                'table': {'headers': ['Record', 'Questions carried with it'],
                          'rows': [['Law and instruments',
                                    'Which jurisdiction, version, commencement and affected '
                                    'provisions?'],
                                   ['Judicial interpretation',
                                    'Which court, issues, reasoning and subsequent treatment?'],
                                   ['International commitments',
                                    'Signature, ratification, entry into force, reservations and '
                                    'domestic implementation?'],
                                   ['Proposed reform',
                                    'Which rights, duties, institutions and dependencies would change?'],
                                   ['Public reflection',
                                    'Whose questions, alternative models and unresolved disagreements '
                                    'remain visible?']]},
                'refs': ['S04', 'S08', 'S09']},
               {'title': "A proposed discussion about Australia's future",
                'text': 'Luke proposes a public examination of Australian law and international '
                        'obligations, leading towards a possible cyber-republic referendum by 2031. In '
                        'this project, cyber-republic refers to a proposed republic supported by '
                        'digital tools for public participation and scrutiny. This is his proposed '
                        'timetable, not an announced referendum.\n'
                        '\n'
                        'Any constitutional change would need to follow the actual parliamentary and '
                        'referendum process. The AEC source explains that process. A model or website '
                        'cannot make the change itself.',
                'refs': ['P03', 'P08', 'S03']},
               {'title': 'Leave room for different views',
                'text': 'People could compare changes with keeping existing arrangements, examine the '
                        'assumptions and disagree with the proposal. Work, healthcare and member '
                        'benefits would not depend on sharing a political view. The term radical '
                        "overcompliance describes the proposal's starting approach: understand and meet "
                        'current obligations while exploring lawful change.'}]},
 {'slug': 'simulation',
  'label': 'Try a simulation',
  'title': 'What depends on what?<br>Try a simple example.',
  'intro': 'If the power goes out, water pumps, food storage and communications may be affected too. A '
           'simulation is a model for exploring connections like these before making changes in the '
           'real world.',
  'image': 'australian-energy',
  'accent': 'mint',
  'tool': 'dependencies',
  'sections': [{'title': 'Look at the connections',
                'text': 'A food business needs water, power, transport, refrigeration and skilled '
                        'people. Changing one part can affect the others. A useful model makes these '
                        'links visible, so people can explore a change and ask what they might have '
                        'missed.',
                'flow': [('Observe', 'Record conditions, origin and credits and what remains unknown.'),
                         ('Model', 'Expose relationships and alternative assumptions.'),
                         ('Rehearse', 'Explore normal operation, changes and disruptions.'),
                         ('Act', 'Authorised people and systems carry out suitable work.'),
                         ('Review', 'Compare the outcome, correct and share agreed learning.')],
                'refs': ['D09', 'P10']},
               {'title': 'Know the limits of a model',
                'text': 'A model can help people ask better questions without predicting everything. It '
                        'needs clear assumptions, information about the real system and checks against '
                        'actual outcomes. A detailed picture of a business or town is not enough to '
                        'show that its predictions are reliable.',
                'cards': [{'title': 'Operating reality',
                           'text': 'What actually exists, who maintains it and what observations '
                                   'support the representation.',
                           'href': None},
                          {'title': 'Alternative futures',
                           'text': 'Changes to staffing, ownership, infrastructure, rules and resource '
                                   'allocation.',
                           'href': None},
                          {'title': 'Contingencies',
                           'text': 'Loss of suppliers, equipment, networks, finance, skills or access '
                                   'to a particular AI service.',
                           'href': None}],
                'refs': ['D03', 'D09']},
               {'title': 'Try a small example',
                'text': 'The example below starts with an electricity interruption because a documented '
                        'South Australian outage shows why power is a useful place to begin. The '
                        'service links in this small model are teaching assumptions, not a '
                        'reconstruction of that event. No live sensors, backup capacity, timing or '
                        'probability are modelled.'},
               {'title': 'Learn from what really happens',
                'text': 'Businesses taking part could test a specific improvement and compare the '
                        'result with the model. They would share only information they were authorised '
                        'to share. Recording failures and unexpected effects would be as useful as '
                        'recording improvements.',
                'refs': ['P02', 'P05', 'D05']}]}])
