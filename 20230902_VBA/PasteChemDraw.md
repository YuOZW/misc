## PowerPoint
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

## Word
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
