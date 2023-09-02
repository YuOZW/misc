## ChemDrawを150%で貼り付け
```
Sub PasteChemDraw()
    ActiveWindow.Selection.SlideRange.Shapes.Paste
    With ActiveWindow.Selection.SlideRange.Shapes(ActiveWindow.Selection.SlideRange.Shapes.Count)
        Select Case .Type
        Case msoEmbeddedOLEObject, msoLinkedOLEObject, msoOLEControlObject, msoLinkedPicture, msoPicture
            .ScaleHeight 1.5, msoTrue
            .ScaleWidth 1.5, msoTrue
        End Select
    End With
End Sub
```
