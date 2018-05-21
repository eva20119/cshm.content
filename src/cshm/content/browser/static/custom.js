$(document).ready(function () {
    count_A = $('#count_A')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_B = $('#count_B')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_C = $('#count_C')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_D = $('#count_D')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_E = $('#count_E')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_F = $('#count_F')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    total_anw = $('#total_anw')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    var chart = c3.generate({
        bindto: '#total_pie',
        size: {
            width: 500,
        },
        data: {
            // iris data from R
            columns: [
                ['5', total_anw[0]],
                ['4', total_anw[1]],
                ['3', total_anw[2]],
                ['2', total_anw[3]],
                ['1', total_anw[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie1',
        size: {
            width: 500,
        },
        data: {
            // iris data from R
            columns: [
                ['5', count_A[0]],
                ['4', count_A[1]],
                ['3', count_A[2]],
                ['2', count_A[3]],
                ['1', count_A[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie2',
        size: {
            width: 500,
        },
        data: {
            // iris data from R
            columns: [
                ['5', count_B[0]],
                ['4', count_B[1]],
                ['3', count_B[2]],
                ['2', count_B[3]],
                ['1', count_B[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie3',
        size: {
            width: 500,
        },
        data: {
            // iris data from R
            columns: [
                ['5', count_C[0]],
                ['4', count_C[1]],
                ['3', count_C[2]],
                ['2', count_C[3]],
                ['1', count_C[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie4',
        size: {
            width: 500,
        },
        data: {
            // iris data from R
            columns: [
                ['5', count_D[0]],
                ['4', count_D[1]],
                ['3', count_D[2]],
                ['2', count_D[3]],
                ['1', count_D[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie5',
        size: {
            width: 500,
        },
        data: {
            // iris data from R
            columns: [
                ['5', count_E[0]],
                ['4', count_E[1]],
                ['3', count_E[2]],
                ['2', count_E[3]],
                ['1', count_E[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie6',
        size: {
            width: 500,
        },
        data: {
            // iris data from R
            columns: [
                ['5', count_F[0]],
                ['4', count_F[1]],
                ['3', count_F[2]],
                ['2', count_F[3]],
                ['1', count_F[4]],
            ],
            type : 'pie',
        }
    });

    each_teacher = JSON.parse($('#each_teacher').text())
    count = 0
    $.each(each_teacher, function(k, v){
        $('#each_teacher_pie').append(`<div id=teacher${count} style="display:inline;margin-bottom:50px"></div>`)
        var chart = c3.generate({
            bindto: '#teacher' + count,
            size: {
                width: 500,
            },
            data: {
                // iris data from R
                columns: [
                    ['5', v[0]],
                    ['4', v[1]],
                    ['3', v[2]],
                    ['2', v[3]],
                    ['1', v[4]],
                ],
                type : 'pie',
            }
        });
        $('#teacher' + count ).prepend(`<h3 style='display:flex;justify-content:center'>${k}</h3>`)        
        count += 1
    })
});

