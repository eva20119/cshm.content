$(function(){
    count_A = $('#count_A')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_B = $('#count_B')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_C = $('#count_C')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_D = $('#count_D')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_E = $('#count_E')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    count_F = $('#count_F')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    total_anw = $('#total_anw')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    envir_data = $('#envir_data')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    space_data = $('#space_data')[0].innerHTML.split(']')[0].split('[')[1].split(',')
    each_teacher = JSON.parse($('#each_teacher').text())
    count = 0

    var chart = c3.generate({
        bindto: '#total_pie',
        size: {
            width: 350,
            height: 350
        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', total_anw[0]],
                ['滿意', total_anw[1]],
                ['尚可', total_anw[2]],
                ['不滿意', total_anw[3]],
                ['非常不滿意', total_anw[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie1',
        size: {
            width: 350,
            height: 350
        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', count_A[0]],
                ['滿意', count_A[1]],
                ['尚可', count_A[2]],
                ['不滿意', count_A[3]],
                ['非常不滿意', count_A[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie2',
        size: {
            width: 350,
            height: 350
        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', count_B[0]],
                ['滿意', count_B[1]],
                ['尚可', count_B[2]],
                ['不滿意', count_B[3]],
                ['非常不滿意', count_B[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie3',
        size: {
            width: 350,
            height: 350
        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', count_C[0]],
                ['滿意', count_C[1]],
                ['尚可', count_C[2]],
                ['不滿意', count_C[3]],
                ['非常不滿意', count_C[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie4',
        size: {
            width: 350,
            height: 350
        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', count_D[0]],
                ['滿意', count_D[1]],
                ['尚可', count_D[2]],
                ['不滿意', count_D[3]],
                ['非常不滿意', count_D[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie5',
        size: {
            width: 350,
            height: 350
        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', count_E[0]],
                ['滿意', count_E[1]],
                ['尚可', count_E[2]],
                ['不滿意', count_E[3]],
                ['非常不滿意', count_E[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie6',
        size: {
            width: 350,
            height: 350

        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', count_F[0]],
                ['滿意', count_F[1]],
                ['尚可', count_F[2]],
                ['不滿意', count_F[3]],
                ['非常不滿意', count_F[4]],
            ],
            type : 'pie',
        }
    });

    var chart = c3.generate({
        bindto: '#pie7',
        size: {
            width: 350,
            height: 350

        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', envir_data[0]],
                ['滿意', envir_data[1]],
                ['尚可', envir_data[2]],
                ['不滿意', envir_data[3]],
                ['非常不滿意', envir_data[4]],
            ],
            type : 'pie',
        }
    });
    var chart = c3.generate({
        bindto: '#pie8',
        size: {
            width: 350,
            height: 350

        },
        data: {
            // iris data from R
            columns: [
                ['非常滿意', space_data[0]],
                ['滿意', space_data[1]],
                ['尚可', space_data[2]],
                ['不滿意', space_data[3]],
                ['非常不滿意', space_data[4]],
            ],
            type : 'pie',
        }
    });

    Object.keys(each_teacher).forEach(function(key){
        $('#each_teacher_pie').append("<div id=teacher" + count + "  style='display:inline;margin-bottom:50px'></div>")

        var chart = c3.generate({
            bindto: '#teacher' + count,
            size: {
                width: 350,
                heiight: 350
            },
            data: {
                // iris data from R
                columns: [
                    ['非常滿意', each_teacher[key][0]],
                    ['滿意', each_teacher[key][1]],
                    ['尚可', each_teacher[key][2]],
                    ['不滿意', each_teacher[key][3]],
                    ['非常不滿意', each_teacher[key][4]],
                ],
                type : 'pie',
            }
        });

        $('#teacher' + count ).prepend("<h3 style='display:flex;justify-content:center'>" + key + "</h3>")        
        count += 1
    })

});


