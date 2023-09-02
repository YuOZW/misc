## ChemDrawを80%で貼り付け
```
Sub PasteChemDraw()
    With Selection
        .PasteSpecial Placement:=wdInLine
        .Start = .Start - 1
        If .InlineShapes.Count = 1 Then
            With .InlineShapes(1)
                .ScaleHeight = 80
                .ScaleWidth = 80
            End With
        End If
    End With
End Sub
```
