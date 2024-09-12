from beaker import *
from pyteal import *

"""
class ApplicationState:
    counter = GlobalStateValue(stack_type=TealType.uint64, default=Int(1))
"""

app = Application("PaperworkAgent")  # , state=ApplicationState)

"""
@app.create(bare=True)
def create() -> Expr:
    return app.initialize_global_state()
"""


@app.delete(bare=True, authorize=Authorize.only(Global.creator_address()))
def delete() -> Expr:
    return Approve()


@app.external
def update_state(
    actual: abi.String, assevered: abi.String, payed: abi.String, *, output: abi.String
) -> Expr:
    return (
        If((actual.get() != assevered.get()) and (actual.get() == payed.get()))
        .Then(output.set("True"))
        .Else(output.set("False"))
    )


if __name__ == "__main__":
    app.build().export("./artifacts")
