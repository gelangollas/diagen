#encoding "utf8"
#GRAMMAR_ROOT S

//разделители: запятая, дефис и двоеточие
Delimiter -> Comma | Hyphen | Colon;

//слово, выполняющее указательную функцию, например: тот, данный, такой и тд.
ComponentPointer -> Word<gram="APRO"> | Word<kwtype="APRO">;

//ключевое слово - тип компонента
ComponentDeclaration -> Word<kwtype="тип_компонента"> interp (Component.Type);

//слова, которые не склоняются и разделители
DescriptionWordCommonPart -> Word<gram="PART"> | Word<gram="PR"> | Word<gram="CONJ"> | Word<gram="INTJ">;

DescriptionWord1 -> Word<gram="gen"> | DescriptionWordCommonPart;
DescriptionWord2 -> Word<gram="nom"> | Word<gram="acc"> | DescriptionWordCommonPart;

//описание компонента
ComponentDescription -> DescriptionWord1+;
//описание действия, выполняемого компонентом
ComponentDescription -> Word<gram="partcp,V"> DescriptionWord2+;
//характеристика компонента
ComponentCharacteristic -> Adj<gram="sg"> interp (Component.Description);

ComponentName -> AnyWord<lat, h-reg1>;

//[указатель][компонент]
Component -> ComponentPointer interp (Component.Pointer=true; Component.Description) ComponentDeclaration {weight = 1.1};
//[компонент][описание компонента] и [компонент][действие][описание действия]
Component -> ComponentDeclaration (Delimiter) ComponentDescription interp (Component.Description);
//[характеристика компонента][компонент]
Component -> ComponentCharacteristic ComponentDeclaration;
//[название компонента на английском]
Component -> ComponentName interp (Component.Name; Component.Type="default");

S -> Component;