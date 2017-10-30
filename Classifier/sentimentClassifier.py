from conceptExtractor import ConceptExtractor


def run():
    concept_extractor = ConceptExtractor()
    text = "i just love brown. gots7"
    concept_extractor.extract_list_of_event_concepts(text)
    #concept_extractor.extract_list_of_object_concepts()

run()
