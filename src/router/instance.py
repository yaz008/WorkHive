from model.keyboard import button_factory
from model.types import User, TempUser
from project.configs import FSAConfig, FSASymbol, FSAState, FSAPipeline
from project.libs.fsa import FSA, serializer
from project.libs.tgdraw import TGMessage


router: FSA[User | TempUser, TGMessage] = FSA(
    routs='router.pipelines',
    button_factory=button_factory,
    initial_transition_state=FSAConfig.InitialTransitionState,
    common_transitions={
        FSAPipeline.Registration: {FSASymbol.Start: FSAState.Register},
        FSAPipeline.Owner: {FSASymbol.Start: FSAState.OwnerMainMenu},
        FSAPipeline.Worker: {FSASymbol.Start: FSAState.WorkerMainMenu},
    },
)


# bool:
@serializer.register_unstructure_hook(bool)
def bool_unstructure_hook(arg: bool) -> str:
    return str(arg)


@serializer.register_structure_hook(bool)
def bool_structure_hook(arg: str) -> bool:
    return arg == 'True'
