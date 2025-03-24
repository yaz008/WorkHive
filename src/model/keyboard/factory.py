from project.configs import WorkHiveButton, FSASymbol
from project.libs.fsa import serializer
from project.libs.tgdraw import ButtonFactory


button_factory: ButtonFactory = ButtonFactory(serialize=serializer.serialize)


button_factory.save(name=WorkHiveButton.Back, symbol=FSASymbol.Back)
button_factory.save(name=WorkHiveButton.Next, symbol=FSASymbol.Next)
button_factory.save(name=WorkHiveButton.Register, symbol=FSASymbol.Next)
button_factory.save(name=WorkHiveButton.Worker, symbol=FSASymbol.InputData)
button_factory.save(name=WorkHiveButton.Owner, symbol=FSASymbol.InputData)
button_factory.save(name=WorkHiveButton.Consent, symbol=FSASymbol.InputData)

button_factory.save(name=WorkHiveButton.NextErr, symbol=FSASymbol.Error)
