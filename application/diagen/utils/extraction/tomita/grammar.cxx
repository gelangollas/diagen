#encoding "utf8"
#GRAMMAR_ROOT S

//разделители: запятая, дефис и двоеточие
Delimiter -> Comma | Hyphen | Colon;

//слово, выполняющее указательную функцию, например: тот, данный, такой и тд.
ComponentPointer -> Word<gram="APRO"> | Word<kwtype="APRO">;

//ключевое слово - тип компонента
ComponentDeclaration -> Word<kwtype="тип_компонента", gram="sg"> interp (Component.Type);
//ключевое слово - тип компонента во множественном числе
ComponentDeclarationPlural -> Word<kwtype="тип_компонента", gram="pl"> interp (Component.Type);

//слова, которые не склоняются и разделители
ServicePartsOfSpeech -> Word<gram="PART"> | Word<gram="PR"> | Word<gram="CONJ"> | Word<gram="INTJ">;
//слова, используемые для описания компонента
DescriptionWord1NotService -> Word<gram="gen", kwtype=~"тип_компонента">;
DescriptionWord1 -> DescriptionWord1NotService | ServicePartsOfSpeech;
DescriptionWord2NotService -> Word<gram="nom", kwtype=~"тип_компонента"> | Word<gram="acc", kwtype=~"тип_компонента">;
DescriptionWord2 -> DescriptionWord2NotService | ServicePartsOfSpeech;

//описание компонента
ComponentDescription -> DescriptionWord1NotService DescriptionWord1* DescriptionWord1NotService | DescriptionWord1* DescriptionWord1NotService | DescriptionWord1NotService;
//описание действия, выполняемого компонентом
ComponentDescription -> Word<gram="partcp,V"> DescriptionWord2* DescriptionWord2NotService;
//характеристика компонента
ComponentCharacteristic -> Adj<gram="sg"> interp (Component.Description);

ComponentName -> AnyWord<lat, h-reg1>+ | AnyWord<h-reg2>;


/*
Далее идут шаблоны для описания компонентов 
*/

//[указатель][компонент]
ComponentNoName -> ComponentPointer interp (Component.Pointer=true; Component.Description) ComponentDeclaration {weight = 1.1};
//[компонент][описание компонента] и [компонент][действие][описание действия]
ComponentNoName -> ComponentDeclaration (Delimiter) ComponentDescription interp (Component.Description);
//[характеристика компонента][компонент]
ComponentNoName -> ComponentCharacteristic ComponentDeclaration;

Component -> ComponentNoName;

//[компонент][название компонента на английском]
Component -> ComponentDeclaration ComponentName interp (Component.Name) (NamedComponentDescription interp (Component.Description));
//[название компонента на английском]
Component -> ComponentName interp (Component.Name);
//[название компонента на английском][-][описание компонента]
Component -> ComponentName interp (Component.Name) (Delimiter) ComponentNoName;
//[описание компонента][-][название компонента на английском]
Component -> ComponentNoName (Delimiter) ComponentName interp (Component.Name);


EnumeratedComponent -> Component;
EnumeratedComponent -> ComponentDescription interp (Component.Description) (ComponentName interp (Component.Name));
EnumeratedComponent -> ComponentName interp (Component.Name; Component.Description=" ");
ComponentsEnumerationEnd -> Comma EnumeratedComponent | "и" EnumeratedComponent;
ComponentsEnumerationPart -> Comma EnumeratedComponent;
ComponentsEnumeration -> EnumeratedComponent ComponentsEnumerationPart* ComponentsEnumerationEnd;
Components -> ComponentDeclarationPlural (Hyphen) (Colon) ComponentsEnumeration;

S -> Component;
S -> Components;